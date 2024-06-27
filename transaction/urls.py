from django.urls import path

from .views import create_payment

urlpatterns = [
    path('create-payment/', create_payment, name='create-payment')
]
