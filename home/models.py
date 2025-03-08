from django.db import models
from django.contrib.auth.models import User
# Donor Model
class DonorRegister(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20) 
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255) 
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)  # Consider using Django's authentication system

    def __str__(self):
        return self.username
    

# Organization Registration Model
class OrganizationRegister(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20) 
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255) 
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)  # Consider using Django's authentication system

    def __str__(self):
        return self.username
    

# Organization Model
class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="organization", default=1)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    place = models.CharField(max_length=255)
    id_proof = models.FileField(upload_to='id_proofs/', null=True, blank=True)

    def __str__(self):
        return self.name


# ✅ Campaign Model (Newly Added)
class Campaign(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="campaigns")  # Linking to Organization
    title = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateField()
    image = models.ImageField(upload_to="campaign_images/", blank=True, null=True)
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
