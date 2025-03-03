from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from .models import DonorRegister
from .forms import DonorRegistrationForm
from .models import OrganizationRegister
from .forms import OrganizationRegistrationForm
from django.urls import reverse
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import OrganizationForm
from .models import Organization
from .models import Campaign
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

def donorlogin(request):
    if request.method == "POST":
        username = request.POST["uname"]
        password = request.POST["password"]
        
        # Check if the username exists
        user = DonorRegister.objects.filter(username=username).first()
        
        # If username doesn't exist or password is incorrect
        if user is None:
            messages.error(request, 'Invalid username or password')
            return redirect('donorlogin')
        elif user.password != password:
            messages.error(request, 'Invalid password')
            return redirect('donorlogin')
        else:
            request.session['uname'] = username
            return redirect('donor')
    return render(request, "donorlogin.html")

def donorlogin_page(request):
    return render(request, 'donorlogin.html')

def donorlogin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Try to authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('donor')  # Redirect to home page or any other page after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'donorlogin.html')
def donorregister(request):
    if request.method == "POST":
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the user data to the database
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('donorlogin')
    else:
        form = DonorRegistrationForm()

    return render(request, 'donorregister.html', {'form': form})


def organizationlogin(request):
    if request.method == "POST":
        username = request.POST["uname"]
        password = request.POST["password"]
        
        # Check if the username exists
        user = OrganizationRegister.objects.filter(username=username).first()
        
        # If username doesn't exist or password is incorrect
        if user is None:
            messages.error(request, 'Invalid username or password')
            return redirect('organizationlogin')
        elif user.password != password:
            messages.error(request, 'Invalid password')
            return redirect('organizationlogin')
        else:
            request.session['uname'] = username
            return redirect('organization')
    return render(request, "organizationlogin.html")

def organizationlogin_page(request):
    return render(request, 'organizationlogin.html')

def organizationlogin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Try to authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('organization')  # Redirect to home page or any other page after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'organizationlogin.html')
def organizationregister(request):
    if request.method == "POST":
        form = OrganizationRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the user data to the database
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('organizationlogin')
    else:
        form = DonorRegistrationForm()

    return render(request, 'organizationregister.html', {'form': form})




def donor(request):
    return render(request, 'donor.html')
def manageprofile(request):
    return render(request, 'manageprofile.html')

def view_campaign(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    campaigns = Campaign.objects.all()  # Fetch all campaigns

    if query:
        campaigns = campaigns.filter(title__icontains=query)  # Filter campaigns by title

    return render(request, 'view_campaign.html', {'campaigns': campaigns, 'query': query})

def makedonation(request):
    return render(request, 'makedonation.html')
def donationhistory(request):
    return render(request, 'donationhistory.html')
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
    organization = get_object_or_404(Organization, id=1)  # Adjust this if multiple organizations exist
    return render(request, 'org_profile.html', {'organization': organization})



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


@login_required
def org_editprofile(request):
    organization = Organization.objects.first()  # Modify this if organizations are user-specific

    if request.method == "POST":
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('org_profile')  # Redirect to profile page after saving
    else:
        form = OrganizationForm(instance=organization)

    return render(request, 'org_editprofile.html', {'form': form})


def admindashboard(request):
    return render(request, 'admin.html')

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required(login_url='adminlogin')
@user_passes_test(is_admin, login_url='adminlogin')
def admin_dashboard(request):
    return render(request, 'admin.html') 