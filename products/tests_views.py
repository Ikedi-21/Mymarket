from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, SellerProfile
from products.models import Product

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller_user = User.objects.create_user(username='seller1', password='ComplexPass123!', role='seller')
        self.seller_profile = SellerProfile.objects.create(user=self.seller_user, display_name='Seller One', bio='Bio')

    def test_product_list_view(self):
        url = reverse('browse')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
