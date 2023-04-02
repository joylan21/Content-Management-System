from django.test import SimpleTestCase
from django.urls import reverse,resolve
from rest_framework_simplejwt.views import TokenRefreshView
from main.views import (
    RegistrationView,
    LoginView,
    content_list_view,
    content_detail_view
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

    def test_content_list_url_is_resolved(self):
        url = reverse('content-list')
        self.assertEquals(resolve(url).func,content_list_view)

    def test_content_detail_url_is_resolved(self):
        url = reverse('content-detail',args=[1])
        self.assertEquals(resolve(url).func,content_detail_view)

    