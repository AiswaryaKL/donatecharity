from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
import razorpay
from .forms import DonorProfileForm
from .models import Feedback
from .forms import FeedbackForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from .models import Complaint
from .forms import ComplaintForm
from .models import DonorRegister
from .forms import DonorRegistrationForm
from .models import OrganizationRegister
from .forms import OrganizationRegistrationForm
from django.urls import reverse
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import OrganizationForm
from .models import Organization
from .models import Campaign,Donation,Donor
from .forms import CampaignForm 


# Create your views here.
def index(request):
    context = {
        # Add any variables you want to pass to the template here
        'product': 'product',
    }
    return render(request,'index.html', context)
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')

def adminlogin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admindashboard')  # Redirect to admin dashboard if already logged in

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin')  # Redirect to admin panel
        else:
            messages.error(request, "Invalid credentials or not an admin user.")
    
    return render(request, 'adminlogin.html')  # Load admin login page


@csrf_exempt
def donorlogin(request):
    if request.method == "POST":
        username = request.POST["uname"]
        password = request.POST["password"]
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('donor')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('donorlogin')
    
    return render(request, "donorlogin.html")
def donorregister(request):
    if request.method == "POST":
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            donor_register = DonorRegister(
                user=user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            donor_register.save()

            # Also create a Donor instance
            donor = Donor.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address']
            )

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('donorlogin')
    else:
        form = DonorRegistrationForm()

    return render(request, 'donorregister.html', {'form': form})
@csrf_exempt
def organizationlogin(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)  # Authenticate the user

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('organization')  # Redirect to organization profile page
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('organizationlogin')

    return render(request, "organizationlogin.html")



def organizationregister(request):
    if request.method == "POST":
        form = OrganizationRegistrationForm(request.POST)
        if form.is_valid():
            # Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            # Save OrganizationRegister and link it to the user
            organization_register = form.save(commit=False)
            organization_register.user = user
            organization_register.password = make_password(form.cleaned_data['password'])  # Secure password
            organization_register.save()

            # Automatically create an Organization profile linked to the user
            Organization.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('organizationlogin')

    else:
        form = OrganizationRegistrationForm()

    return render(request, 'organizationregister.html', {'form': form})


def donor(request):
    campaigns = Campaign.objects.all()
    print(campaigns)  # Debugging: See if campaigns are fetched
    return render(request, 'donor.html', {'campaigns': campaigns})

@login_required
def donor_profile(request):
    user = request.user

    # Fetch the donor profile linked to the logged-in user
    donor = Donor.objects.filter(user=user).first()

    if not donor:
        return render(request, 'donor_profile.html', {'error': "No donor profile found!"})

    return render(request, 'donor_profile.html', {'donor': donor})
@login_required
def manageprofile(request):
    user = request.user

    # Fetch donor profile
    donor = Donor.objects.filter(user=user).first()

    if not donor:
        messages.error(request, "No donor profile found!")
        return redirect('donor_profile')

    if request.method == "POST":
        form = DonorProfileForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('donor_profile')
    else:
        form = DonorProfileForm(instance=donor)

    return render(request, 'manageprofile.html', {'form': form})

def view_campaign(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    campaigns = Campaign.objects.all()  # Fetch all campaigns

    if query:
        campaigns = campaigns.filter(title__icontains=query)  # Filter campaigns by title

    return render(request, 'view_campaign.html', {'campaigns': campaigns, 'query': query})



def makedonation(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    if request.method == "POST":
        amount = int(request.POST.get("amount")) * 100  # Convert to paise
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        return render(request, 'makedonation.html', {
            'campaign': campaign,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'order_id': payment['id'],
            'amount': amount
        })

    return render(request, 'makedonation.html', {'campaign': campaign, 'razorpay_key': settings.RAZORPAY_KEY_ID})




@login_required
def payment_success(request):
    payment_id = request.GET.get("payment_id")
    campaign_id = request.GET.get("campaign_id")
    amount = request.GET.get("amount")

    if not (payment_id and campaign_id and amount):
        return redirect('home')  # Redirect if any required param is missing

    campaign = get_object_or_404(Campaign, id=campaign_id)

    # Ensure the user is authenticated
    if request.user.is_authenticated:
        donation = Donation.objects.create(
            user=request.user,
            campaign=campaign,
            amount=float(amount) / 100,  # Convert paise to INR
            payment_id=payment_id
        )

    return render(request, 'payment_success.html')

def donationhistory(request):
    donations = Donation.objects.filter(user=request.user).order_by('-date')
    return render(request, 'donationhistory.html', {'donations': donations})

def donorfeedback(request):
    return render(request, 'donorfeedback.html')
def donorcomplaint(request):
    return render(request, 'donorcomplaint.html')
def charityreport(request):
    return render(request, 'charityreport.html')

def custom_logout_view(request):
    logout(request)  # Logs out the user
    return redirect('/home/')

def organization(request):
    return render(request, 'organization.html') 
def organization(request):
    return render(request, 'organization.html')

@login_required
def org_profile(request):
    user = request.user

    # Fetch the organization linked to the logged-in user
    organization = Organization.objects.filter(user=user).first()

    if not organization:
        return render(request, 'org_profile.html', {'error': "No organization profile found!"})

    return render(request, 'org_profile.html', {'organization': organization})
@login_required
def org_editprofile(request):
    user = request.user

    # Get the registered organization details
    organization = Organization.objects.filter(user=user).first()
    org_register = OrganizationRegister.objects.filter(user=user).first()

    if request.method == "POST":
        organization.name = request.POST.get("name", organization.name)
        organization.email = request.POST.get("email", organization.email)
        organization.phone = request.POST.get("phone", organization.phone)
        organization.address = request.POST.get("address", organization.address)
        organization.place = request.POST.get("place", organization.place)

        # Handle ID Proof upload
        if request.FILES.get("id_proof"):
            organization.id_proof = request.FILES["id_proof"]

        organization.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("org_profile")

    return render(request, "org_editprofile.html", {
        "organization": organization,
        "org_register": org_register
    })



def create_campaign(request):
    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)

        if form.is_valid():
            campaign = form.save(commit=False)  # Don't save to DB yet

            # Ensure user has an organization before assigning
            if hasattr(request.user, "organization"):
                campaign.organization = request.user.organization  # Assign org
                campaign.save()
                messages.success(request, "Campaign successfully created! 🚀")
                return redirect("campaign_list")  # Redirect after saving
            else:
                form.add_error(None, "You are not associated with any organization.")

    else:
        form = CampaignForm()

    return render(request, "create_campaign.html", {"form": form})

def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, "campaign_list.html", {"campaigns": campaigns})





def is_admin(user):
    return user.is_authenticated and user.is_superuser

def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("admindashboard")  # Redirect to the admin dashboard
        else:
            return render(request, "adminlogin.html", {"error": "Invalid credentials or not an admin"})

    return render(request, "adminlogin.html")  # Show login form if GET request

@login_required(login_url="adminlogin")
@user_passes_test(is_admin, login_url="adminlogin")
def admindashboard(request):
    return render(request, "admin.html")

@login_required
def admin_logout(request):
    logout(request)
    return redirect("adminlogin")


@login_required
def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Your feedback has been submitted successfully!")
            return redirect('feedback_success')  # Redirect to feedback success page
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form})

@login_required
def viewfeedback(request):
    if not request.user.is_superuser:  # Only admin can view
        return redirect('home')

    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'viewfeedback.html', {'feedbacks': feedbacks})

def feedback_success(request):
    return render(request, 'feedback_success.html')

@login_required
def submit_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user

            # Set user_type correctly
            if request.user.groups.filter(name='Donor').exists():
                complaint.user_type = 'donor'
            elif request.user.groups.filter(name='Organization').exists():
                complaint.user_type = 'organization'
            else:
                complaint.user_type = 'donor'  # Default to donor if no group found

            complaint.save()
            messages.success(request, "Your complaint has been submitted successfully!")
            return redirect('complaint_list')

    else:
        form = ComplaintForm()

    return render(request, 'submit_complaint.html', {'form': form})

@login_required
def complaint_list(request):
    """Show complaints submitted by the logged-in user."""
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'complaint_list.html', {'complaints': complaints})
@login_required
def admin_complaints(request):
    if not request.user.is_superuser:
        messages.warning(request, "You do not have permission to access this page.")
        return redirect('donor')

    # Fetch complaints and log the output
    complaints = Complaint.objects.all().order_by('-created_at')

    # Debugging: Print complaints to console
    print(f"Admin Complaints - Total Complaints: {complaints.count()}")
    for complaint in complaints:
        print(f"Complaint ID: {complaint.id}, User: {complaint.user.username}, UserType: {complaint.user_type}, Subject: {complaint.subject}, Status: {complaint.status}")

    return render(request, 'admin_complaints.html', {'complaints': complaints})

@login_required
def respond_complaint(request, complaint_id):
    """Allow admin to respond to complaints."""
    if not request.user.is_superuser:
        return redirect('donor')

    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == "POST":
        response = request.POST.get("response")
        complaint.response = response
        complaint.status = True  # Mark as resolved
        complaint.save()
        messages.success(request, "Complaint responded successfully.")
        return redirect('admin_complaints')

    return render(request, 'respond_complaint.html', {'complaint': complaint})

@csrf_exempt  # Temporarily disable CSRF for testing (not recommended in production)
def donorlogout(request):
    if request.method == "POST" or request.method == "GET":  # Allow GET for logout
        logout(request)
        return redirect('donorlogin')  # Redirect to the login page
    return redirect('donor')  # Redirect back to donor profile if method is not allowed