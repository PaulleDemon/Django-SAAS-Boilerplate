from django.urls import path

from .views import create_payment, pricing


urlpatterns = [
    path('pricing/', pricing, name='pricing'),
    path('create-payment/', create_payment, name='create-payment'),
]
