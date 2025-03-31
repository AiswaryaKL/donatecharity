from django.contrib import admin
from .models import DonorRegister
from .models import OrganizationRegister
from .models import Organization,Campaign
from .models import Donation,Donor,Feedback,Complaint

# Register your models here.
class DonorRegisterAdmin(admin.ModelAdmin):
    list_display=('name','phone','email','address','username')
    search_fields=('gender',)
admin.site.register(DonorRegister,DonorRegisterAdmin)

class OrganizationRegisterAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'phone', 'address')  # Columns displayed in admin panel
    search_fields = ('username', 'name', 'email')  # Search functionality
    list_filter = ('name',)  # Filter options in the sidebar
    ordering = ('username',)  # Default ordering
    readonly_fields = ('password',)  # Prevent editing password directly (consider using Django auth system)

admin.site.register(OrganizationRegister, OrganizationRegisterAdmin)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "place")  # Columns displayed in admin list view
    search_fields = ("name", "email", "phone", "place")  # Searchable fields
    list_filter = ("place",)  # Filter organizations by place
    ordering = ("name",)  # Default ordering by name



class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'goal_amount', 'raised_amount', 'status', 'verified', 'is_edit_pending', 'end_date', 'created_at')
    list_filter = ('status', 'verified', 'is_edit_pending', 'organization', 'end_date')
    search_fields = ('title', 'organization__name')
    actions = ['mark_as_completed', 'mark_as_verified']

    @admin.action(description='Mark selected campaigns as Completed')
    def mark_as_completed(self, request, queryset):
        for campaign in queryset:
            if campaign.raised_amount >= campaign.goal_amount:
                campaign.status = 'Completed'
                campaign.save()
            else:
                self.message_user(request, f"Cannot complete {campaign.title} as it hasn't reached the goal amount.")
    
    @admin.action(description='Mark selected campaigns as Verified')
    def mark_as_verified(self, request, queryset):
        queryset.update(verified=True)
        self.message_user(request, "Selected campaigns marked as Verified.")
    
admin.site.register(Campaign, CampaignAdmin)

# Donation Admin
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'amount', 'payment_id', 'date')
    list_filter = ('date', 'campaign')
    search_fields = ('user__username', 'campaign__title', 'payment_id')
    readonly_fields = ('date',)
admin.site.register(Donation, DonationAdmin)

class DonorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'phone', 'total_donations')
    search_fields = ('user__username', 'name', 'email', 'phone')
    list_filter = ('total_donations',)
    ordering = ('user',)
    
admin.site.register(Donor, DonorAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'rating', 'created_at')  # Show in admin list
    list_filter = ('user_type', 'rating', 'created_at')  # Filter options
    search_fields = ('user__username', 'message')  # Searchable fields
    ordering = ('-created_at',)  # Newest feedback first
    readonly_fields = ('created_at',)  # Prevent modification of timestamp

admin.site.register(Feedback, FeedbackAdmin)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'status', 'created_at')
    search_fields = ('user__username', 'subject', 'message')
    list_filter = ('status', 'user_type')





