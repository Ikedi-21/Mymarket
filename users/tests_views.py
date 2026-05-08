from django.test import TestCase, Client
from django.urls import reverse
from users.models import User

class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_buyer(self):
        url = reverse('register')
        data = {
            'username': 'buyer1',
            'email': 'buyer1@example.com',
            'role': 'buyer',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='buyer1').exists())

    def test_login_redirect_seller(self):
        User.objects.create_user(username='seller2', password='ComplexPass123!', role='seller')
        url = reverse('login')
        data = {'username': 'seller2', 'password': 'ComplexPass123!'}
        response = self.client.post(url, data)
        # We need to mock seller_dashboard or have it exist
        self.assertEqual(response.status_code, 302)
