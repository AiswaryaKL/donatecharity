from django.contrib import admin
from .models import DonorRegister
from .models import OrganizationRegister
from .models import Organization,Campaign
from .models import Donation

# Register your models here.
class DonorRegisterAdmin(admin.ModelAdmin):
    list_display=('name','phone','email','address','username')
    search_fields=('gender',)
admin.site.register(DonorRegister,DonorRegisterAdmin)

class OrganizationRegisterAdmin(admin.ModelAdmin):
    list_display=('name','phone','email','address','username')
    search_fields=('gender',)
admin.site.register(OrganizationRegister,OrganizationRegisterAdmin)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "place")  # Columns displayed in admin list view
    search_fields = ("name", "email", "phone", "place")  # Searchable fields
    list_filter = ("place",)  # Filter organizations by place
    ordering = ("name",)  # Default ordering by name

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "goal_amount", "end_date", "created_at")  # Display these columns
    search_fields = ("title", "organization__name")  # Allow search by title and organization name
    list_filter = ("end_date", "organization")  # Filter campaigns by end date and organization
    date_hierarchy = "end_date"  # Adds a date-based navigation bar

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'amount', 'payment_id', 'date')
    search_fields = ('user__username', 'campaign__title', 'payment_id')
    list_filter = ('date', 'campaign')
    ordering = ('-date',)




