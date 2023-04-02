from django.test import SimpleTestCase
from django.urls import reverse,resolve
from rest_framework_simplejwt.views import TokenRefreshView
from main.views import (
    RegistrationView,
    LoginView,
    content_list_view,
    content_detail_view,
    content_create_view,
    content_update_view,
    content_delete_view,
    category_list_view,
    category_detail_view,
    category_create_view,
    category_delete_view
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

    def test_content_create_url_is_resolved(self):
        url = reverse('content-create')
        self.assertEquals(resolve(url).func,content_create_view)

    def test_content_update_url_is_resolved(self):
        url = reverse('content-update',args=[1])
        self.assertEquals(resolve(url).func,content_update_view)

    def test_content_delete_url_is_resolved(self):
        url = reverse('content-delete',args=[1])
        self.assertEquals(resolve(url).func,content_delete_view)

    def test_category_list_url_is_resolved(self):
        url = reverse('category-list')
        self.assertEquals(resolve(url).func,category_list_view)

    def test_category_detail_url_is_resolved(self):
        url = reverse('category-detail',args=[1])
        self.assertEquals(resolve(url).func,category_detail_view)

    def test_category_create_url_is_resolved(self):
        url = reverse('category-create')
        self.assertEquals(resolve(url).func,category_create_view)

    def test_category_delete_url_is_resolved(self):
        url = reverse('category-delete',args=[1])
        self.assertEquals(resolve(url).func,category_delete_view)


    