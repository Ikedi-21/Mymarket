from django.test import TestCase
from users.forms import RegistrationForm

class RegistrationFormTest(TestCase):
    def test_buyer_registration_valid(self):
        data = {
            'username': 'testbuyer',
            'email': 'buyer@example.com',
            'role': 'buyer',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_seller_registration_missing_fields(self):
        data = {
            'username': 'testseller',
            'email': 'seller@example.com',
            'role': 'seller',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('display_name', form.errors)
        self.assertIn('bio', form.errors)
