from django.db import models
from django.conf import settings
from products.models import Product
import uuid
from django.utils import timezone
from datetime import timedelta

class Order(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.product.title}"

class Download(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='download')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    downloaded = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Download for {self.order.product.title}"
