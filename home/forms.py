from django import forms
from .models import DonorRegister
from .models import Organization,Campaign,Donor,Feedback,Complaint


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
        if not phone.isdigit() or len(phone) < 10:
            raise forms.ValidationError("Enter a valid phone number with at least 10 digits.")
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
        if not phone.isdigit() or len(phone) < 10:
            raise forms.ValidationError("Enter a valid phone number with at least 10 digits.")
        return phone

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'phone', 'address', 'place', 'id_proof']


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'goal_amount', 'end_date', 'image']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'phone', 'email', 'address', 'date_of_birth']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['user_type', 'message', 'rating']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'message']