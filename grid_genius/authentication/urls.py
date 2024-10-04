
from django.urls import path,include
from authentication.views import *
from . import views

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
]