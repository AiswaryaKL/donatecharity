from django.urls import path
from.import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.index,name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('donorregister/',views.donorregister,name='donorregister'),
    path('donorlogin.html', views.donorlogin, name='donorlogin'),
    path('donorlogin/', views.donorlogin_view, name='donorlogin_post'),
    path('organizationregister/',views.organizationregister,name='organizationregister'),
    path('organizationlogin.html', views.organizationlogin, name='organizationlogin'),
    path('organizationlogin/', views.organizationlogin_view, name='organizationbnlogin_post'),
    path('logout/', LogoutView.as_view(next_page='/home/'), name='logout'),
    path('donor/', views.donor, name='donor'),
    path('manageprofile/', views.manageprofile, name='manageprofile'),
    path('view_campaign/', views.view_campaign, name='view_campaign'),
    path('makedonation/', views.makedonation, name='makedonation'),
    path('donationhistory/', views.donationhistory, name='donationhistory'),
    path('donorfeedback/', views.donorfeedback, name='donorfeedback'),
    path('donorcomplaint/', views.donorcomplaint, name='donorcomplaint'),
    path('charityreport/', views.charityreport, name='charityreport'),
    path('organization/', views.organization, name='organization'),
    path('org_profile/', views.org_profile, name='org_profile'),
    path('create_campaign/', views.create_campaign, name='create_campaign'),
    path("campaigns/", views.campaign_list, name="campaign_list"),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('org_editprofile/', views.org_editprofile, name='org_editprofile'),

]