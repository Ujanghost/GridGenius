from django.urls import path
from .views import predictor, formInfo

urlpatterns = [
    path('', predictor, name='predictor'),  # Home page
    path('form-info/', formInfo, name='formInfo'),
        # Add this line
]