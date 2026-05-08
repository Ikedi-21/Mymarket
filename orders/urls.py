from django.urls import path
from .views import CreateCheckoutSessionView, PaymentSuccessView, MyPurchasesView, OrdersReceivedView
from .views_download import SecureDownloadView

urlpatterns = [
    path('checkout/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('download/<uuid:token>/', SecureDownloadView.as_view(), name='secure_download'),
    path('my-purchases/', MyPurchasesView.as_view(), name='my_purchases'),
    path('received/', OrdersReceivedView.as_view(), name='orders_received'),
]
