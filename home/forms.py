from django import forms
from .models import DonorRegister
from .models import Organization,Campaign,Donor,Feedback,Complaint
from datetime import date
import re

class DonorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = DonorRegister
        fields = ['name', 'email', 'phone', 'username', 'password', 'address']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("The name should contain only alphabetic characters.")
        if len(name) < 3:
            raise forms.ValidationError("The name should be at least 3 characters long.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if DonorRegister.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if DonorRegister.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone.isdigit() or len(phone) != 10:
             raise forms.ValidationError("Please enter a valid 10-digit phone number.")
        if phone[0] not in ('9', '8', '7', '6'):
             raise forms.ValidationError("Phone number must start with 9, 8, 7, or 6.")
        return phone


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone = forms.CharField(max_length=15, required=True)

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("The name should contain only alphabetic characters.")
        if len(name) < 3:
            raise forms.ValidationError("The name should be at least 3 characters long.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError("This field is required.")
        return email

    def clean_address(self):
        address = self.cleaned_data.get('address', '').strip()
        if not address:
            raise forms.ValidationError("This field is required.")
        return address

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        if phone[0] not in ('9', '8', '7', '6'):
            raise forms.ValidationError("Phone number must start with 9, 8, 7, or 6.")
        return phone



from .models import OrganizationRegister


class OrganizationRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = OrganizationRegister
        fields = ['name', 'email', 'phone', 'username', 'password', 'address']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("The name should contain only alphabetic characters.")
        if len(name) < 3:
            raise forms.ValidationError("The name should be at least 3 characters long.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if OrganizationRegister.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if OrganizationRegister.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit phone number.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone = forms.CharField(max_length=15, required=True)

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("The name should contain only alphabetic characters.")
        if len(name) < 3:
            raise forms.ValidationError("The name should be at least 3 characters long.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError("This field is required.")
        return email

    def clean_address(self):
        address = self.cleaned_data.get('address', '').strip()
        if not address:
            raise forms.ValidationError("This field is required.")
        return address

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        if phone[0] not in ('9', '8', '7', '6'):
            raise forms.ValidationError("Phone number must start with 9, 8, 7, or 6.")
        return phone

from django import forms
from .models import Organization, Campaign, Donor, Feedback, Complaint

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'phone', 'address', 'place', 'id_proof']

    # Validate Name
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name should contain only letters and spaces.")
        return name

    # Validate Email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Organization.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Only Gmail addresses are allowed.")
        return email

    # Validate Phone
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        if phone[0] not in ('9', '8', '7', '6'):
            raise forms.ValidationError("Phone number must start with 9, 8, 7, or 6.")
        return phone

    # Validate Address
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 10:
            raise forms.ValidationError("Address must be at least 10 characters long.")
        return address

    # Validate Place
    def clean_place(self):
        place = self.cleaned_data.get('place')
        if not place.replace(" ", "").isalpha():
            raise forms.ValidationError("Place should contain only letters and spaces.")
        return place

    # Validate ID Proof
    def clean_id_proof(self):
        id_proof = self.cleaned_data.get('id_proof')
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
        if not id_proof:
            raise forms.ValidationError("Please upload a valid ID proof.")
        if not any(id_proof.name.lower().endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError("Only PDF, JPG, JPEG, or PNG files are allowed.")
        if id_proof.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError("File size must not exceed 5MB.")
        return id_proof
class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'goal_amount', 'end_date', 'image']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title').strip()
    
        if not title:
            raise forms.ValidationError("Title cannot be empty or contain only spaces.")
        if len(title) < 5 or len(title) > 100:
            raise forms.ValidationError("Title must be between 5 and 100 characters.")
        if not re.match(r'^[A-Za-z\s.,!?;:\-\'"]+$', title):
            raise forms.ValidationError("Title can only contain letters, spaces, and punctuation (.,!?;:'\"-).")

        return title


    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description.strip():
            raise forms.ValidationError("Description cannot be empty or contain only spaces.")
        if len(description) < 20:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        if not re.match(r'^[A-Za-z\s.,!?]+$', description):
            raise forms.ValidationError("Description can only contain letters, spaces, and punctuation.")
        return description

    def clean_goal_amount(self):
        goal_amount = self.cleaned_data.get('goal_amount')
        if goal_amount is None:
            raise forms.ValidationError("Goal amount is required.")
        if not str(goal_amount).isdigit():
            raise forms.ValidationError("Goal amount must be a numeric value.")
        if goal_amount <= 0:
            raise forms.ValidationError("Goal amount must be greater than zero.")
        return goal_amount

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date <= date.today():
            raise forms.ValidationError("End date must be a future date.")
        return end_date

  

class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'phone', 'email', 'address', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name should only contain alphabets and spaces.")
        if len(name) < 2 or len(name) > 100:
            raise forms.ValidationError("Name must be between 2 and 100 characters.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError("Enter a valid phone number with 10 to 15 digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email cannot be empty.")
        return email

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 5 or len(address) > 255:
            raise forms.ValidationError("Address must be between 5 and 255 characters.")
        return address

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        today = date.today()

        if not date_of_birth:
            raise forms.ValidationError("Date of Birth is required.")
        if date_of_birth > today:
            raise forms.ValidationError("Date of Birth cannot be in the future.")
        if (today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))) < 18:
            raise forms.ValidationError("You must be at least 18 years old.")
        
        return date_of_birth

class DonorFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message', 'rating']

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise forms.ValidationError("Message is required.")
        if not re.match(r'^[A-Za-z\s]+$', message.strip()):
            raise forms.ValidationError("Message should contain only letters and spaces.")
        return message

class OrganizationFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message', 'rating']

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise forms.ValidationError("Message is required.")
        if not re.match(r'^[A-Za-z\s]+$', message.strip()):
            raise forms.ValidationError("Message should contain only letters and spaces.")
        return message

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'message']

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if not subject.replace(' ', '').isalpha():
            raise forms.ValidationError("Subject can only contain letters and spaces.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message.replace(' ', '').isalpha():
            raise forms.ValidationError("Message can only contain letters and spaces.")
        return message
