from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, SellerProfile
from products.models import Product
from orders.models import Order, Download

class OrderHistoryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller_user = User.objects.create_user(username='seller1', password='ComplexPass123!', role='seller')
        self.seller_profile = SellerProfile.objects.create(user=self.seller_user, display_name='Seller One', bio='Bio')
        self.product = Product.objects.create(seller=self.seller_profile, title='Test Product', price=10, category='file', is_active=True)
        self.buyer_user = User.objects.create_user(username='buyer1', password='ComplexPass123!', role='buyer')
        self.order = Order.objects.create(buyer=self.buyer_user, product=self.product, amount_paid=10, is_paid=True)
        self.download = Download.objects.create(order=self.order)

    def test_my_purchases_view(self):
        self.client.login(username='buyer1', password='ComplexPass123!')
        url = reverse('my_purchases')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_orders_received_view(self):
        self.client.login(username='seller1', password='ComplexPass123!')
        url = reverse('orders_received')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'buyer1')
