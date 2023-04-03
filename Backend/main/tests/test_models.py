from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from main.models import User, Category, Content
from django.core.files.base import ContentFile


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@test.com',
            'full_name': 'Test User',
            'phone': '1234567890',
            'address': 'Test Address',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'pincode': '123456'
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.full_name, self.user_data['full_name'])
        self.assertEqual(user.phone, self.user_data['phone'])
        self.assertEqual(user.address, self.user_data['address'])
        self.assertEqual(user.city, self.user_data['city'])
        self.assertEqual(user.state, self.user_data['state'])
        self.assertEqual(user.country, self.user_data['country'])
        self.assertEqual(user.pincode, self.user_data['pincode'])
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(**self.user_data, password='password')
        self.assertEqual(superuser.email, self.user_data['email'])
        self.assertEqual(superuser.full_name, self.user_data['full_name'])
        self.assertEqual(superuser.phone, self.user_data['phone'])
        self.assertEqual(superuser.address, self.user_data['address'])
        self.assertEqual(superuser.city, self.user_data['city'])
        self.assertEqual(superuser.state, self.user_data['state'])
        self.assertEqual(superuser.country, self.user_data['country'])
        self.assertEqual(superuser.pincode, self.user_data['pincode'])
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category_name = 'Test Category'

    def test_create_category(self):
        category = Category.objects.create(name=self.category_name)
        self.assertEqual(category.name, self.category_name)

class ContentModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@test.com',
            'full_name': 'Test User',
            'phone': '1234567890',
            'address': 'Test Address',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'pincode': '123456'
        }
        self.category_name = 'Test Category'
        self.category = Category.objects.create(name=self.category_name)
        self.pdf_file = ContentFile(b'This is a dummy PDF file.')

    def test_create_content(self):
        user = User.objects.create_user(**self.user_data)
        content = Content.objects.create(title='Test Title', body='Test Body', summary='Test Summary', pdf_file=self.pdf_file, author=user)
        content.categories.add(self.category)
        self.assertEqual(content.title, 'Test Title')
        self.assertEqual(content.body, 'Test Body')
        self.assertEqual(content.summary, 'Test Summary')
        self.assertEqual(content.author, user)
        self.assertEqual(list(content.categories.all()), [self.category])
