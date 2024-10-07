
from django.urls import path,include
from authentication.views import *
from . import views
from django.contrib.auth import views as auth_views

app_name = "authentication" 

urlpatterns = [
  
  path("",home,name="home"),
  # path("signup/",,name='authView'),
  path("accounts/",include("django.contrib.auth.urls")),
  path('about/', about_view, name='about'),  # About page
  path('contact/', contact_view, name='contact'),  # Contact page
  path('service/', service_view, name='service'),  # Services page
  path('portfolio/', portfolio_view, name='portfolio'),  # Services page
  path('signup/', signup, name='signup'),
  path('login/', login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),

    # Password Reset URLs
      path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             email_template_name='registration/password_reset_email.html',
             template_name='registration/password_reset_form.html',
             subject_template_name='registration/password_reset_subject.txt',
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),

    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
 
]