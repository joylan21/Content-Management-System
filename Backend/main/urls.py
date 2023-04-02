from django.urls import path
from .views import RegistrationView
from .views import LoginView

urlpatterns = [
    
    # api for user registration
    path('register/', RegistrationView.as_view(), name='register'),

    # api for user login
    path('login/', LoginView.as_view(), name='login'),
]