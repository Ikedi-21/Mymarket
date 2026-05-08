from django.db import models
from users.models import SellerProfile

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('file', 'File'),
        ('template', 'Template'),
        ('course', 'Course'),
    )

    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    thumbnail = models.ImageField(upload_to='product_thumbnails/')
    product_file = models.FileField(upload_to='product_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
