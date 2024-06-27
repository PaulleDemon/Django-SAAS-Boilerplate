from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model

from payments import PurchasedItem
from payments.models import BasePayment

User = get_user_model()


class Plan(models.Model):

    name = models.CharField(max_length=150) # name of your plan
    description = models.CharField(max_length=150) # small description of the plan

    price = models.DecimalField(max_digits=9, decimal_places=2, default="0.0")

    features = models.TextField(null=True, blank=True)

    datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name}'

    def features_as_list(self):
        
        if self.features:
            return self.features.replace(" ", "").split(",")

        return []

class Transaction(BasePayment):

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.SET_NULL)

    def get_failure_url(self) -> str:
        # Return a URL where users are redirected after
        # they fail to complete a payment:
        return f"http://localhost:8000/payments/{self.pk}/failure"

    def get_success_url(self) -> str:
        # Return a URL where users are redirected after
        # they successfully complete a payment:
        return f"http://localhost:8000/payments/{self.pk}/success"

    def get_purchased_items(self):
        # Return items that will be included in this payment.
        yield PurchasedItem(
            name='The Hound of the Baskervilles',
            sku='BSKV',
            quantity=9,
            price=Decimal(10),
            currency='USD',
        )