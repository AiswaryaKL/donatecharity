from django.urls import path
from.import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.index,name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('donorregister/',views.donorregister,name='donorregister'),
    path('donorlogin/', views.donorlogin, name='donorlogin'),
    path('organizationregister/',views.organizationregister,name='organizationregister'),
    path('organizationlogin/', views.organizationlogin, name='organizationlogin'),
    path('logout/', LogoutView.as_view(next_page='/home/'), name='logout'),
    path('donor/', views.donor, name='donor'),
    path('donor_profile/', views.donor_profile, name='donor_profile'),
    path('manageprofile/', views.manageprofile, name='manageprofile'),
    path('view_campaign/', views.view_campaign, name='view_campaign'),
    path('makedonation/<int:campaign_id>/', views.makedonation, name='makedonation'),
    path('donationhistory/', views.donationhistory, name='donationhistory'),
    path('donorfeedback/', views.donorfeedback, name='donorfeedback'),
    path('donorcomplaint/', views.donorcomplaint, name='donorcomplaint'),
    path('charityreport/', views.charityreport, name='charityreport'),
    path('organization/', views.organization, name='organization'),
    path('org_profile/', views.org_profile, name='org_profile'),
    path('create_campaign/', views.create_campaign, name='create_campaign'),
    path("campaigns/", views.campaign_list, name="campaign_list"),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path("admin_logout/", views.admin_logout, name="admin_logout"),
    
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('org_editprofile/', views.org_editprofile, name='org_editprofile'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('viewfeedback/', views.viewfeedback, name='viewfeedback'),
    path('feedback_success', views.feedback_success, name='feedback_success'),
    path('donorfeedback_success', views.donorfeedback_success, name='donorfeedback_success'),
    path('admin/', views.admin_complaints, name='admin_complaints'),  # Ensure correct mapping
    path('respond/<int:complaint_id>/', views.respond_complaint, name='respond_complaint'),
    path('logout/', views.donorlogout, name='donorlogout'),
    path("edit/<int:campaign_id>/", views.edit_campaign, name="edit_campaign"),
    path('donations/', views.track_donations, name='track_donations'),
    path('organizationlogout/', views.organizationlogout, name='organizationlogout'),
    path('organization_donations/', views.organization_donations, name='organization_donations'),
    path('charity-report/', views.charity_report, name="charity_report"),
    path('donor_feedback/', views.donor_feedback, name='donor_feedback'),
    path('organization_feedback/', views.organization_feedback, name='organization_feedback'),
    path('submit_donor_complaint/', views.submit_donor_complaint, name='submit_donor_complaint'),
    path('donor_complaint_list/', views.donor_complaint_list, name='donor_complaint_list'),
    path('submit_org_complaint/', views.submit_org_complaint, name='submit_org_complaint'),
    path('org_complaint_list/', views.org_complaint_list, name='org_complaint_list'),


]