from django.db import models
from django.contrib.auth.models import User

# Donor Model
class DonorRegister(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20) 
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255) 
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)  # Consider using Django's authentication system

    def __str__(self):
        return self.username
    

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="donor")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20) 
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)  # Added Date of Birth
    total_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  

    def __str__(self):
        return self.user.username
    
# Organization Registration Model

class OrganizationRegister(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20) 
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255) 
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Using Django's authentication

    def __str__(self):
        return self.username

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="organization", null=True, blank=True)  
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    place = models.CharField(max_length=255, blank=True, null=True)
    id_proof = models.FileField(upload_to='id_proofs/', null=True, blank=True)

    def __str__(self):
        return self.name




# ✅ Campaign Model (Newly Added)
class Campaign(models.Model):
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="campaigns"
    )  
    title = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateField()
    image = models.ImageField(upload_to="campaign_images/", blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="campaigns", null=True, blank=True
    )  # Temporarily allow null values
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.date}"
    
class Feedback(models.Model):
    USER_TYPES = [
        ('donor', 'Donor'),
        ('organization', 'Organization'),
    ]

    RATING_CHOICES = [(i, f"{i} ⭐") for i in range(1, 6)]  # 1 to 5 stars

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    message = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)  # Default 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.user_type}) - {self.rating} Stars - {self.created_at}"


class Complaint(models.Model):
    USER_TYPES = [
        ('donor', 'Donor'),
        ('organization', 'Organization'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)  # False means not responded yet

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.subject}"
    
class CharityReport(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="charity_reports")
    total_donations = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    num_donors = models.IntegerField(default=0)
    num_campaigns = models.IntegerField(default=0)
    month = models.IntegerField()  # Stores the month number (1-12)
    year = models.IntegerField()  # Stores the year
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'month', 'year')  # Ensure only one report per month per organization

    def __str__(self):
        return f"Report for {self.organization.name} - {self.month}/{self.year}"