from django.test import TestCase
from users.models import User, SellerProfile
from products.models import Product
from orders.models import Order, Download
from django.utils import timezone
from datetime import timedelta

class DownloadModelTest(TestCase):
    def setUp(self):
        self.seller_user = User.objects.create_user(username='seller1', password='ComplexPass123!', role='seller')
        self.seller_profile = SellerProfile.objects.create(user=self.seller_user, display_name='Seller One', bio='Bio')
        self.product = Product.objects.create(seller=self.seller_profile, title='Test Product', price=10, category='file', is_active=True)
        self.buyer_user = User.objects.create_user(username='buyer1', password='ComplexPass123!', role='buyer')
        self.order = Order.objects.create(buyer=self.buyer_user, product=self.product, amount_paid=10, is_paid=True)

    def test_download_creation(self):
        download = Download.objects.create(order=self.order)
        self.assertIsNotNone(download.token)
        self.assertIsNotNone(download.expires_at)
        self.assertFalse(download.is_expired())

    def test_download_expiry(self):
        download = Download.objects.create(order=self.order)
        download.expires_at = timezone.now() - timedelta(hours=1)
        download.save()
        self.assertTrue(download.is_expired())
