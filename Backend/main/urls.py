from django.urls import path
from .views import RegistrationView
from .views import (
    LoginView,
    content_list_view,
    content_detail_view,
    )

urlpatterns = [
    
    # api for user registration
    path('register/', RegistrationView.as_view(), name='register'),

    # api for user login
    path('login/', LoginView.as_view(), name='login'),

    # content URLs
    path('contents/', content_list_view, name='content-list'),
    path('contents/<int:pk>/', content_detail_view, name='content-detail'),
]