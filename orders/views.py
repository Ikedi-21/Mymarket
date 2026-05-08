from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.urls import reverse
from products.models import Product
from .models import Order, Download
from services.stripe import create_checkout_session, verify_checkout_session
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        if request.user.role == 'seller' and product.seller.user == request.user:
            return redirect('product_detail', pk=pk)
        if request.user.role != 'buyer':
             return redirect('product_detail', pk=pk)
        success_url = request.build_absolute_uri(reverse('payment_success'))
        cancel_url = request.build_absolute_uri(reverse('product_detail', args=[pk]))
        session_id, session_url = create_checkout_session(product, success_url, cancel_url, request.user.email)
        if session_id:
            return redirect(session_url)
        return redirect('product_detail', pk=pk)

class PaymentSuccessView(LoginRequiredMixin, View):
    def get(self, request):
        session_id = request.GET.get('session_id')
        if not session_id:
            return redirect('browse')
        session = verify_checkout_session(session_id)
        if session and session.payment_status == 'paid':
            product_id = session.metadata['product_id']
            product = get_object_or_404(Product, pk=product_id)
            order, created = Order.objects.get_or_create(
                stripe_payment_intent=session.payment_intent,
                defaults={'buyer': request.user, 'product': product, 'amount_paid': product.price, 'is_paid': True}
            )
            if created:
                Download.objects.get_or_create(order=order)
            return render(request, 'orders/payment_success.html', {'order': order})
        return redirect('browse')

class MyPurchasesView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/my_purchases.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user, is_paid=True).order_by('-created_at')

class OrdersReceivedView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/orders_received.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.role != 'seller':
            return Order.objects.none()
        return Order.objects.filter(product__seller=self.request.user.seller_profile, is_paid=True).order_by('-created_at')
