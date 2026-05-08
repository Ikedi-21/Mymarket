from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, SellerProfile
from products.models import Product
from orders.models import Order, Download
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

class SecureDownloadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller_user = User.objects.create_user(username='seller1', password='ComplexPass123!', role='seller')
        self.seller_profile = SellerProfile.objects.create(user=self.seller_user, display_name='Seller One', bio='Bio')

        # We need a real file for FileResponse
        self.product_file = SimpleUploadedFile("test.zip", b"content", content_type="application/zip")
        self.product = Product.objects.create(
            seller=self.seller_profile,
            title='Test Product',
            price=10,
            category='file',
            is_active=True,
            product_file=self.product_file
        )

        self.buyer_user = User.objects.create_user(username='buyer1', password='ComplexPass123!', role='buyer')
        self.other_buyer = User.objects.create_user(username='buyer2', password='ComplexPass123!', role='buyer')

        self.order = Order.objects.create(buyer=self.buyer_user, product=self.product, amount_paid=10, is_paid=True)
        self.download = Download.objects.create(order=self.order)

    def test_download_success(self):
        self.client.login(username='buyer1', password='ComplexPass123!')
        url = reverse('secure_download', args=[self.download.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')

    def test_download_wrong_user(self):
        self.client.login(username='buyer2', password='ComplexPass123!')
        url = reverse('secure_download', args=[self.download.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_download_expired(self):
        self.download.expires_at = timezone.now() - timedelta(hours=1)
        self.download.save()
        self.client.login(username='buyer1', password='ComplexPass123!')
        url = reverse('secure_download', args=[self.download.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "expired", status_code=403)
