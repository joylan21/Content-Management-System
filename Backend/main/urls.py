from django.urls import path
from .views import RegistrationView
from .views import (
    LoginView,
    content_list_view,
    content_detail_view,
    content_create_view,
    content_update_view,
    content_delete_view,
    category_list_view,
    )

urlpatterns = [
    
    # api for user registration
    path('register/', RegistrationView.as_view(), name='register'),

    # api for user login
    path('login/', LoginView.as_view(), name='login'),

    # content URLs
    path('contents/', content_list_view, name='content-list'),
    path('contents/<int:pk>/', content_detail_view, name='content-detail'),
    path('contents/create/', content_create_view, name='content-create'),
    path('contents/<int:pk>/update/', content_update_view, name='content-update'),
    path('contents/<int:pk>/delete/', content_delete_view, name='content-delete'),

    # Category URLs
    path('categories/', category_list_view, name='category-list'),
]