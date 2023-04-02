from django.test import SimpleTestCase
from django.urls import reverse,resolve
from rest_framework_simplejwt.views import TokenRefreshView
from main.views import (
    RegistrationView,
    LoginView
)

class TestUrls(SimpleTestCase):
    
    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class,RegistrationView)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class,LoginView)

    def test_refresh_token_url_is_resolved(self):
        url = reverse('token_refresh')
        self.assertEquals(resolve(url).func.view_class,TokenRefreshView)