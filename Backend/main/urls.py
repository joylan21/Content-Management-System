from django.urls import path
from .views import RegistrationView

urlpatterns = [
    
    # api for user registration
    path('register/', RegistrationView.as_view(), name='register'),
]