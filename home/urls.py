from django.contrib import admin
from django.urls import path,include
from home import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',views.index,name='home'),
    path('2 After Login.html',views.loginUser,name='loginUser'),
    path('sign_up.html',views.sign_up,name='sign_up'),
    path('1 Before Login.html',views.logoutUser,name='logout'),
    path("3 Rolling.html",views.rolling,name='rolling'),
    path("4 faculty.html",views.faculty,name='faculty'),
    path("5 account.html",views.myAccount,name='myAccount'), 
    path("contact.html",views.contact,name='contact'),
    path("PAGE 1 OF 8.html",views.page1,name='page1'),
    path("PAGE 2 OF 8.html",views.page2,name='page2'),
    path("PAGE 3 OF 8.html",views.page3,name='page3'),
    path("PAGE 4 OF 8.html",views.page4,name='page4'),
    path("PAGE 6 OF 8.html",views.page6,name='page6'),
    path("PAGE 7 OF 8.html",views.page7,name='page7'),
    path("PAGE 8 OF 8.html",views.page8,name='page8'),
    path("roll_adv.html",views.roll_adv,name='roll_adv'),
    path("faculty_adv.html",views.faculty_adv,name='faculty_adv'),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
         name='password_reset'),
    path('password_reset_done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),


     
     #     path('save-draft1/', views.save_draft1, name='save_draft1'),
    path('form-page1/', views.load_form_page1, name='form_page1'),
     #     path('save-draft2/', views.save_draft2, name='save_draft2'),
    path('form-page2/', views.load_form_page2, name='form_page2'),
     #     path('save-draft3/', views.save_draft3, name='save_draft3'),
    path('form-page3/', views.load_form_page3, name='form_page3'),
     #     path('save-draft4/', views.save_draft4, name='save_draft4'),
    path('form-page4/', views.load_form_page4, name='form_page4'),
     #     path('save-draft5/', views.save_draft5, name='save_draft5'),
    path('form-page5/', views.load_form_page5, name='form_page5'),
     #     path('save-draft6/', views.save_draft6, name='save_draft6'),
    path('form-page6/', views.load_form_page6, name='form_page6'),
     #     path('save-draft7/', views.save_draft7, name='save_draft7'),
    path('form-page7/', views.load_form_page7, name='form_page7'),
    path('save_draft1/', views.basicDetails, name='save_draft1'),#edited for submit
    path('save_draft2/', views.communicationDetails, name='save_draft2'),#edited for submit
    path('save_draft3/', views.educationDetails, name='save_draft3'),#edited for submit
    path('save_draft4/', views.experienceDetails, name='save_draft4'),#edited for submit
    path('save_draft6/', views.otherDetails, name='save_draft6'),#edited for submit
    path('Submit/', views.generalDetails, name='Submit'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 