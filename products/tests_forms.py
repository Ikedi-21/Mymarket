from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from products.forms import ProductForm
from PIL import Image
import io

class ProductFormTest(TestCase):
    def test_product_form_valid(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)

        thumbnail = SimpleUploadedFile("thumb.png", file.read(), content_type="image/png")
        product_file = SimpleUploadedFile("product.zip", b"content", content_type="application/zip")
        data = {
            'title': 'Test Product',
            'description': 'Description',
            'price': '10.00',
            'category': 'template',
            'is_active': True,
        }
        form = ProductForm(data=data, files={'thumbnail': thumbnail, 'product_file': product_file})
        self.assertTrue(form.is_valid(), form.errors)
