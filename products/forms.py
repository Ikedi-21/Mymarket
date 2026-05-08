from django import forms
from .models import Product
import os

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'thumbnail', 'product_file', 'is_active']

    def clean_product_file(self):
        file = self.cleaned_data.get('product_file')
        if file:
            extension = os.path.splitext(file.name)[1].lower()
            allowed_extensions = ['.pdf', '.zip', '.docx', '.mp4', '.png', '.jpg', '.jpeg']
            if extension not in allowed_extensions:
                raise forms.ValidationError(f"Unsupported file extension. Allowed: {', '.join(allowed_extensions)}")
        return file
