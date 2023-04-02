from django.test import TestCase, Client
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from main.models import User, Content, Category
from main.serializers import UserSerializer, ContentSerializer, ContentViewSerializer
from django.urls import reverse
import json

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