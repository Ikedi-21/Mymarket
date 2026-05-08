from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Product
from .forms import ProductForm

class SellerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'seller'

class SellerDashboardView(SellerRequiredMixin, ListView):
    model = Product
    template_name = 'products/seller_dashboard.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user.seller_profile)

class ProductCreateView(SellerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('seller_dashboard')

    def form_valid(self, form):
        form.instance.seller = self.request.user.seller_profile
        return super().form_valid(form)

class ProductUpdateView(SellerRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('seller_dashboard')

    def test_func(self):
        product = self.get_object()
        return super().test_func() and product.seller == self.request.user.seller_profile

class ProductDeleteView(SellerRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('seller_dashboard')

    def test_func(self):
        product = self.get_object()
        return super().test_func() and product.seller == self.request.user.seller_profile

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Product.CATEGORY_CHOICES
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'featured_products'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('-created_at')[:6]
