from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
import razorpay
from django.db.models import F,Q
from .forms import DonorProfileForm
from django.utils import timezone
from django.db import models
from .models import Donation
from datetime import datetime
from datetime import date
from .models import Feedback
from .forms import DonorFeedbackForm, OrganizationFeedbackForm
from django.utils.timezone import now
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
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
            # Ensure user is a donor (by checking the Donor model)
            if hasattr(user, 'donor'):
                login(request, user)
                return redirect('donor')
            else:
                messages.error(request, 'You are not registered as a donor.')
                return redirect('donorlogin')
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

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Ensure user is an organization (by checking the Organization model)
            if hasattr(user, 'organization'):
                login(request, user)
                return redirect('organization')
            else:
                messages.error(request, 'You are not registered as an organization.')
                return redirect('organizationlogin')
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

    # ✅ Get the number of donations made by the donor
    total_donations = Donation.objects.filter(user=user).count()

    return render(request, 'donor_profile.html', {'donor': donor, 'total_donations': total_donations})

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
            messages.success(request, "")
            return redirect('donor_profile')  # ✅ Redirect to donor_profile page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DonorProfileForm(instance=donor)

    return render(request, 'manageprofile.html', {'form': form})
@login_required
def view_campaign(request):
    # Update campaign status
    Campaign.objects.filter(
        (Q(raised_amount__gte=F('goal_amount')) | Q(end_date__lt=timezone.now())) & Q(status="Ongoing")
    ).update(status="Completed")

    # Fetch only verified campaigns
    campaigns = Campaign.objects.filter(verified=True).order_by('-created_at')

    # Check if donor profile is complete
    try:
        donor_profile = Donor.objects.get(user=request.user)  # Refresh from DB
        required_fields = [
            donor_profile.name,
            donor_profile.phone,
            donor_profile.email,
            donor_profile.address,
            donor_profile.date_of_birth,
        ]
        # Ensure all fields are filled and donor is at least 18
        profile_complete = all(required_fields)
        if donor_profile.date_of_birth:
            today = date.today()
            age = today.year - donor_profile.date_of_birth.year - (
                (today.month, today.day) < (donor_profile.date_of_birth.month, donor_profile.date_of_birth.day)
            )
            if age < 18:
                profile_complete = False
    except Donor.DoesNotExist:
        profile_complete = False

    return render(request, 'view_campaign.html', {
        'campaigns': campaigns,
        'profile_complete': profile_complete,
    })


def makedonation(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    # Calculate the remaining goal amount (goal - raised)
    raised_amount = Donation.objects.filter(campaign=campaign).aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
    remaining_goal = campaign.goal_amount - raised_amount

    if request.method == "POST":
        try:
            amount = int(request.POST.get("amount"))

            # Check if donation exceeds the remaining goal amount
            if amount > remaining_goal:
                messages.error(request, f"Donation amount cannot exceed the remaining goal amount of ₹{remaining_goal}.")
                return render(request, 'makedonation.html', {
                    'campaign': campaign,
                    'razorpay_key': settings.RAZORPAY_KEY_ID,
                    'remaining_goal': remaining_goal
                })

            # Convert to paise (Razorpay uses the smallest currency unit)
            amount_in_paise = amount * 100

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": "1"
            })

            return render(request, 'makedonation.html', {
                'campaign': campaign,
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'order_id': payment['id'],
                'amount': amount_in_paise,
                'remaining_goal': remaining_goal
            })

        except ValueError:
            messages.error(request, "Please enter a valid amount.")
            return render(request, 'makedonation.html', {
                'campaign': campaign,
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'remaining_goal': remaining_goal
            })

    return render(request, 'makedonation.html', {
        'campaign': campaign,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'remaining_goal': remaining_goal
    })

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
        messages.success(request, "")
        return redirect("org_profile")

    return render(request, "org_editprofile.html", {
        "organization": organization,
        "org_register": org_register
    })



@login_required
def create_campaign(request):
    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)

            if hasattr(request.user, "organization"):
                campaign.organization = request.user.organization
                campaign.created_by = request.user
                campaign.save()

                messages.success(request, "")
                return redirect("campaign_list")
            else:
                messages.error(request, "You are not associated with any organization.")
                return redirect("create_campaign")

    else:
        form = CampaignForm()

    return render(request, "create_campaign.html", {"form": form})

@login_required
def campaign_list(request):
    campaigns = Campaign.objects.filter(created_by=request.user)

    # Calculate raised amount for each campaign
    for campaign in campaigns:
        campaign.raised_amount = campaign.donation_set.aggregate(Sum('amount'))['amount__sum'] or 0
        campaign.progress_percentage = (campaign.raised_amount / campaign.goal_amount) * 100 if campaign.goal_amount > 0 else 0
    
    return render(request, "campaign_list.html", {"campaigns": campaigns})
@login_required
def edit_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id, created_by=request.user)

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            campaign.is_edit_pending = True
            campaign.verified = False  # Require re-verification
            form.save()
            messages.info(request, "")
            return redirect("campaign_list")
    else:
        form = CampaignForm(instance=campaign)

    return render(request, "edit_campaign.html", {"form": form, "campaign": campaign})




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
    return redirect("home")


def donor_feedback(request):
    if request.method == 'POST':
        form = DonorFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.user_type = 'donor'
            feedback.save()
            messages.success(request, "")
            return redirect('donorfeedback_success')  # Redirect to feedback success page
    else:
        form = DonorFeedbackForm()
    return render(request, 'donor_feedback.html', {'form': form})


def donorfeedback_success(request):
    return render(request, 'donorfeedback_success.html')

def organization_feedback(request):
    if request.method == 'POST':
        form = OrganizationFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.user_type = 'organization'
            feedback.save()
            messages.success(request, "")
            return redirect('feedback_success')  # Redirecting to feedback success page
    else:
        form = OrganizationFeedbackForm()
    return render(request, 'organization_feedback.html', {'form': form})




@login_required
def viewfeedback(request):
    if not request.user.is_superuser:  # Only admin can view
        return redirect('home')

    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'viewfeedback.html', {'feedbacks': feedbacks})

def feedback_success(request):
    return render(request, 'feedback_success.html')

@login_required
def submit_donor_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.user_type = 'donor'
            complaint.save()
            messages.success(request, "")
            return redirect('donor_complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'submit_donor_complaint.html', {'form': form})

@login_required
def donor_complaint_list(request):
    complaints = Complaint.objects.filter(user=request.user, user_type='donor').order_by('-created_at')
    return render(request, 'donor_complaint_list.html', {'complaints': complaints})


@login_required
def submit_org_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.user_type = 'organization'
            complaint.save()
            messages.success(request, "")
            return redirect('org_complaint_list')
        else:
            messages.error(request, "There was an error submitting the complaint. Please check the form.")
    else:
        form = ComplaintForm()

    return render(request, 'submit_org_complaint.html', {'form': form})


@login_required
def org_complaint_list(request):
    complaints = Complaint.objects.filter(user=request.user, user_type='organization').order_by('-created_at')
    return render(request, 'org_complaint_list.html', {'complaints': complaints})


@login_required
def admin_complaints(request):
    """Admin view to see all complaints from donors and organizations."""
    if not request.user.is_superuser:
        messages.warning(request, "You do not have permission to access this page.")
        return redirect('donor')

    # Fetch all complaints along with user details
    complaints = Complaint.objects.select_related('user').all().order_by('-created_at')

    # Correctly determine user type
    for complaint in complaints:
        if hasattr(complaint.user, 'user_type'):  # Ensure the user has a user_type field
            complaint.user_type_display = (
                "Organization" if complaint.user.user_type.lower() == "organization" else "Donor"
            )
        else:
            complaint.user_type_display = "Unknown"

    return render(request, 'admin_complaints.html', {'complaints': complaints})


@login_required
def respond_complaint(request, complaint_id):
    """Allow admin to respond to a complaint."""
    if not request.user.is_superuser:
        return redirect('donor')

    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == "POST":
        response = request.POST.get("response")
        complaint.response = response
        complaint.status = True  # Mark as resolved
        complaint.save()
        messages.success(request, "")
        return redirect('admin_complaints')

    return render(request, 'respond_complaint.html', {'complaint': complaint})

@csrf_exempt  # Temporarily disable CSRF for testing (not recommended in production)
def donorlogout(request):
    if request.method == "POST" or request.method == "GET":  # Allow GET for logout
        logout(request)
        return redirect('donorlogin')  # Redirect to the login page
    return redirect('donor')  # Redirect back to donor profile if method is not allowed

@staff_member_required  # Restricts access to admins only
def track_donations(request):
    donations = Donation.objects.all().order_by('-date')

    # Filtering donations based on user input
    donor_name = request.GET.get('donor_name', '')
    if donor_name:
        donations = donations.filter(user__username__icontains=donor_name)

    campaign_name = request.GET.get('campaign_name', '')
    if campaign_name:
        donations = donations.filter(campaign__title__icontains=campaign_name)

    return render(request, 'track_donations.html', {'donations': donations}) 

@csrf_exempt  # Temporarily disable CSRF for testing (not recommended in production)
def organizationlogout(request):
    if request.method == "POST" or request.method == "GET":  # Allow GET for logout
        logout(request)
        return redirect('organizatiologin')  # Redirect to the login page
    return redirect('organization')  # Redirect back to donor profile if method is not allowed

@login_required
def organization_donations(request):
    """Fetch donations for campaigns owned by the logged-in organization."""
    organization = request.user.organization  # Assuming User is linked to Organization

    # Get all campaigns belonging to the organization
    campaigns = Campaign.objects.filter(organization=organization)

    # Get all donations for these campaigns
    donations = Donation.objects.filter(campaign__in=campaigns).order_by('-date')

    context = {
        "donations": donations,
        "organization": organization
    }
    return render(request, "organization_donations.html", context)

@login_required
def verify_campaigns(request):
    if not request.user.is_superuser:
        messages.error(request, "Access Denied!")
        return redirect('home')

    campaigns = Campaign.objects.filter(models.Q(verified=False) | models.Q(is_edit_pending=True))
    return render(request, 'verify_campaigns.html', {'campaigns': campaigns})

@login_required
def approve_campaigns(request, campaign_id):
    if not request.user.is_superuser:
        messages.error(request, "Access Denied!")
        return redirect('home')

    campaign = get_object_or_404(Campaign, id=campaign_id)
    campaign.verified = True
    campaign.is_edit_pending = False
    campaign.save()
    messages.success(request, f"Campaign '{campaign.title}' has been approved.")
    return redirect('verify_campaigns')

@login_required
def reject_campaigns(request, campaign_id):
    if not request.user.is_superuser:
        messages.error(request, "Access Denied!")
        return redirect('home')

    campaign = get_object_or_404(Campaign, id=campaign_id)
    if campaign.is_edit_pending:
        campaign.is_edit_pending = False
        campaign.verified = True  # Revert to previous verified version
        campaign.save()
        messages.success(request, f"Campaign edits for '{campaign.title}' have been rejected.")
    else:
        campaign.delete()
        messages.success(request, f"Campaign '{campaign.title}' has been rejected.")
    return redirect('verify_campaigns')



def generate_report(request):
    selected_month = request.GET.get('month')

    if not selected_month:
        return render(request, 'charity_report.html', {'error': 'Please select a month to generate the report.'})

    try:
        year, month = map(int, selected_month.split('-'))
        start_date = timezone.make_aware(datetime(year, month, 1))
        if month == 12:
            end_date = timezone.make_aware(datetime(year + 1, 1, 1))
        else:
            end_date = timezone.make_aware(datetime(year, month + 1, 1))

        # ✅ Fetch Donations and Campaigns
        donations = Donation.objects.filter(date__gte=start_date, date__lt=end_date).select_related('campaign', 'user')
        campaigns = Campaign.objects.filter(created_at__gte=start_date, created_at__lt=end_date)

        # ✅ Calculate Total Donations and Total Donors
        total_donations = donations.aggregate(total=Sum('amount'))['total'] or 0
        total_donors = donations.values('user').distinct().count()

        # ✅ Calculate Raised Amount for Each Campaign with Status
        campaign_data = []
        for campaign in campaigns:
            raised_amount = Donation.objects.filter(campaign=campaign).aggregate(total_raised=Sum('amount'))['total_raised'] or 0
            campaign_data.append({
                'title': campaign.title,
                'goal_amount': campaign.goal_amount,
                'raised_amount': raised_amount,
                'organization': campaign.organization.name,
                'status': campaign.status,  # ✅ Include Status
            })

        # ✅ Group Campaigns by Organization
        org_campaign_data = {}
        for data in campaign_data:
            org_name = data['organization']
            if org_name not in org_campaign_data:
                org_campaign_data[org_name] = []
            org_campaign_data[org_name].append(data)

        context = {
            'selected_month': selected_month,
            'donations': donations,
            'org_campaign_data': [{'organization': org, 'campaigns': campaigns} for org, campaigns in org_campaign_data.items()],
            'total_donations': total_donations,
            'total_donors': total_donors,
        }
        return render(request, 'generate_report.html', context)

    except ValueError:
        return render(request, 'charity_report.html', {'error': 'Invalid month format. Please try again.'})

def charity_report(request):
    return render(request, 'charity_report.html')