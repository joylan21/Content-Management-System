from django.test import TestCase, Client
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from main.models import User, Content, Category
from main.serializers import UserSerializer, ContentSerializer, ContentViewSerializer
from django.urls import reverse
from rest_framework.test import APIClient
import json
from django.core.files.base import ContentFile
from unittest.mock import patch

with open('/home/joy/WORK_DIR/care24/Content-Management-System/Backend/main/tests/dummy.pdf', 'rb') as f:
    dummy_pdf_content = f.read()
dummy_pdf_file = ContentFile(dummy_pdf_content)

client = Client()

class RegistrationViewTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            'email': 'testuser@test.com',
            'full_name': 'Test User',
            'phone': 1234567890,
            'address': 'Test Address',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'pincode': 123456,
            'password': 'Testpass@123'
        }
        self.invalid_payload = {
            'email': 'testuser@test.com',
            'full_name': 'Test User',
            'phone': 1234567890,
            'address': 'Test Address',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'pincode': 123456
        }
        
    def test_registration_with_valid_payload(self):
        response = client.post(
            reverse('register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_with_invalid_payload(self):
        response = client.post(
            reverse('register'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_password_less_than_8(self):
        self.valid_payload['password']='passwor'
        response = client.post(
            reverse('register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_password_no_uppercase(self):
        self.valid_payload['password']='password@123'
        response = client.post(
            reverse('register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_password_no_lowercase(self):
        self.valid_payload['password']='PASSWORD@123'
        response = client.post(
            reverse('register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_no_numeric_phone(self):
        self.valid_payload['phone']='phone45455'
        response = client.post(
            reverse('register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_with_no_numeric_pin(self):
        self.valid_payload['pincode']='pin455'
        response = client.post(
            reverse('register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_with_no_email(self):
        del self.valid_payload['email']
        response = client.post(
            reverse('register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@test.com',
            full_name='Test User',
            phone=1234567890,
            address='Test Address',
            city='Test City',
            state='Test State',
            country='Test Country',
            pincode=123456,
            password='Testpass@123'
        )
        self.valid_payload = {
            'email': 'testuser@test.com',
            'password': 'Testpass@123'
        }
        self.invalid_payload = {
            'email': 'testuser@test.com',
            'password': 'wrongpass'
        }

    def test_login_with_valid_credentials(self):
        response = client.post(
            reverse('login'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        response = client.post(
            reverse('login'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ContentListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testemail@test.com',
            password='testpassword123',
            full_name='Test User'
        )
        self.superuser = User.objects.create_superuser(
            email='testemail2@test.com',
            password='testpassword123',
            full_name='Test User'
        )
        self.category = Category.objects.create(name='Test Category')
        self.content_data = {
            "title": "Test Title",
            "body": "Test Body",
            "summary": "Test Summary",
            'pdf_file':open('/home/joy/WORK_DIR/care24/Content-Management-System/Backend/main/tests/dummy.pdf', 'rb'),
            "categories": [self.category.id]
        }
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

    def test_content_list_view_with_authenticated_user(self):
        Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        response = self.client.get(reverse('content-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_content_list_view_with_unauthenticated_user(self):
        self.client.credentials()  # remove authentication credentials
        response = self.client.get(reverse('content-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_content_list_view_with_search_query(self):
        response = self.client.get(reverse('content-list') + '?query=' + 'hello')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('main.views.Content.objects.all')
    def test_content_list_view_exception_handling(self, mock_filter):
        mock_filter.side_effect = Exception('Something went wrong')
        response = self.client.get(reverse('content-list'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_content_detail_view_with_authenticated_user(self):
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-detail', kwargs={'pk': content.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_content_detail_view_with_admin_user(self):
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-detail', kwargs={'pk': content.id})
        refresh = RefreshToken.for_user(self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_content_detail_view_with_unauthenticated_user(self):
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-detail', kwargs={'pk': content.id})
        self.client.credentials() # remove authentication credentials
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('main.views.Content.objects.all')
    def test_content_detail_view_exception_handling(self, mock_filter):
        mock_filter.side_effect = Exception('Something went wrong')
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-detail', kwargs={'pk': content.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_content_create_view_with_authenticated_user(self):
        response = self.client.post(reverse('content-create'), data=self.content_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_content_create_view_with_invalid_data(self):
        response = self.client.post(reverse('content-create'), data={}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_content_create_view_with_unauthenticated_user(self):
        self.client.credentials() # remove authentication credentials
        response = self.client.post(reverse('content-create'), data=self.content_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('main.views.ContentViewSerializer.is_valid')
    def test_content_create_view_exception_handling(self, mock_filter):
        mock_filter.side_effect = Exception('Something went wrong')
        response = self.client.post(reverse('content-create'), data=self.content_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_content_update_view_with_unauthenticated_user(self):
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-update', kwargs={'pk': content.id})
        self.client.credentials() # remove authentication credentials
        response = self.client.put(url, data=self.content_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_content_update_view_with_authenticated_user(self):
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-update', kwargs={'pk': content.id})
        response = self.client.put(url, data=self.content_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_content_update_view_with_invalid_data(self):
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-update', kwargs={'pk': content.id})
        response = self.client.put(url, data={'pdf_file':''}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_content_update_view_with_admin_user(self):
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-update', kwargs={'pk': content.id})
        refresh = RefreshToken.for_user(self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        response = self.client.put(url, data=self.content_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('main.views.ContentViewSerializer.is_valid')
    def test_content_update_view_exception_handling(self, mock_filter):
        mock_filter.side_effect = Exception('Something went wrong')
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-update', kwargs={'pk': content.id})
        response = self.client.put(url, data=self.content_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_content_delete_view_with_authenticated_user(self):
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-delete', kwargs={'pk': content.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_content_delete_view_with_admin_user(self):
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-delete', kwargs={'pk': content.id})
        refresh = RefreshToken.for_user(self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_content_delete_view_with_unauthenticated_user(self):
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-delete', kwargs={'pk': content.id})
        self.client.credentials() # remove authentication credentials
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('main.views.Content.objects.all')
    def test_content_delete_view_exception_handling(self, mock_filter):
        mock_filter.side_effect = Exception('Something went wrong')
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=dummy_pdf_file, author=self.user)
        url = reverse('content-delete', kwargs={'pk': content.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_list_view_with_authenticated_user(self):
        response = self.client.get(
            reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_list_view_with_unauthenticated_user(self):
        self.client.credentials()
        response = self.client.get(
            reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('main.views.Category.objects.all')
    def test_content_category_list_view_exception_handling(self, mock_filter):
        mock_filter.side_effect = Exception('Something went wrong')
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_detail_view_with_authenticated_user(self):
        response = self.client.get(
            reverse('category-detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_detail_view_with_unauthenticated_user(self):
        self.client.credentials()
        response = self.client.get(
            reverse('category-detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('main.views.Category.objects.all')
    def test_content_category_detail_view_exception_handling(self, mock_filter):
        mock_filter.side_effect = Exception('Something went wrong')
        response = self.client.get(
            reverse('category-detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_create_view_with_authenticated_user(self):
        data = {'name': 'test_category'}
        response = self.client.post(reverse('category-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_category_create_view_with_invalid_data(self):
        data = {}
        response = self.client.post(reverse('category-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_create_view_with_unauthenticated_user(self):
        self.client.credentials()
        data = {'name': 'test_category'}
        response = self.client.post(reverse('category-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('main.views.CategorySerializer.is_valid')
    def test_content_category_create_view_exception_handling(self, mock_filter):
        mock_filter.side_effect = Exception('Something went wrong')
        data = {'name': 'test_category'}
        response = self.client.post(reverse('category-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_delete_view_with_authenticated_user(self):
        response = self.client.delete(
            reverse('category-delete', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_delete_view_with_unauthenticated_user(self):
        self.client.credentials()
        response = self.client.delete(
            reverse('category-delete', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('main.views.Category.objects.all')
    def test_content_delete_create_view_exception_handling(self, mock_filter):
        mock_filter.side_effect = Exception('Something went wrong')
        response = self.client.delete(
            reverse('category-delete', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
