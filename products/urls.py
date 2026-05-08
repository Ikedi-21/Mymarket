from django.urls import path
from .views import (
    SellerDashboardView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    ProductListView, ProductDetailView
)

urlpatterns = [
    path('browse/', ProductListView.as_view(), name='browse'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('seller/dashboard/', SellerDashboardView.as_view(), name='seller_dashboard'),
    path('seller/product/new/', ProductCreateView.as_view(), name='product_create'),
    path('seller/product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('seller/product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
