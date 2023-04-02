from django.test import SimpleTestCase
from django.urls import reverse,resolve

from main.views import (
    RegistrationView,
)

class TestUrls(SimpleTestCase):
    
    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class,RegistrationView)

