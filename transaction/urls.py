from django.urls import path

from .views import (create_payment, pricing, 
                        payment_failed, payment_success)

from .webhooks import stripe_webhook

urlpatterns = [
    path('pricing/', pricing, name='pricing'),
    path('create-payment/', create_payment, name='create-payment'),
    

    path('payment/failed/', payment_failed, name='payment-failed'),
    path('payment/success/', payment_success, name='payment-success'),
    path('stripe/webhook/', stripe_webhook, name='webhook'),
]
