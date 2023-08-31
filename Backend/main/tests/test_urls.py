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
    
    # Test if the register URL resolves to the RegistrationView class
    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class,RegistrationView)

    # Test if the login URL resolves to the LoginView class
    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class,LoginView)

    # Test if the token refresh URL resolves to the TokenRefreshView class
    def test_refresh_token_url_is_resolved(self):
        url = reverse('token_refresh')
        self.assertEquals(resolve(url).func.view_class,TokenRefreshView)

    # Test if the content list URL resolves to the content_list_view function
    def test_content_list_url_is_resolved(self):
        url = reverse('content-list')
        self.assertEquals(resolve(url).func,content_list_view)

    # Test if the content detail URL with a primary key resolves to the content_detail_view function
    def test_content_detail_url_is_resolved(self):
        url = reverse('content-detail',args=[1])
        self.assertEquals(resolve(url).func,content_detail_view)

    # Test if the content create URL resolves to the content_create_view function
    def test_content_create_url_is_resolved(self):
        url = reverse('content-create')
        self.assertEquals(resolve(url).func,content_create_view)

    # Test if the content update URL with a primary key resolves to the content_update_view function
    def test_content_update_url_is_resolved(self):
        url = reverse('content-update',args=[1])
        self.assertEquals(resolve(url).func,content_update_view)

    # Test if the content delete URL with a primary key resolves to the content_delete_view function
    def test_content_delete_url_is_resolved(self):
        url = reverse('content-delete',args=[1])
        self.assertEquals(resolve(url).func,content_delete_view)

    # Test if the category list URL resolves to the category_list_view function
    def test_category_list_url_is_resolved(self):
        url = reverse('category-list')
        self.assertEquals(resolve(url).func,category_list_view)

    # Test if the category detail URL with a primary key resolves to the category_detail_view function
    def test_category_detail_url_is_resolved(self):
        url = reverse('category-detail',args=[1])
        self.assertEquals(resolve(url).func,category_detail_view)

    # Test if the category create URL resolves to the category_create_view function
    def test_category_create_url_is_resolved(self):
        url = reverse('category-create')
        self.assertEquals(resolve(url).func,category_create_view)

    # Test if the category delete URL with a primary key resolves to the category_delete_view function
    def test_category_delete_url_is_resolved(self):
        url = reverse('category-delete',args=[1])
        self.assertEquals(resolve(url).func,category_delete_view)


    