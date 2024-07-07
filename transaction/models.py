from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from payments import PurchasedItem
from payments.models import BasePayment

from utils.money import cents_to_dollar, dollar_to_cents

User = get_user_model()


class SUBSCRIPTION_STATUS(models.IntegerChoices):

    INACTIVE  = (0, 'inactive')
    ACTIVE  = (1, 'active')
    CANCELLED = (2, 'cancelled')


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
            return [x.strip() for x in self.features.split(",")]

        return []
    
    def get_total_cents(self):
        # converts  dollar to cents.

        return dollar_to_cents(self.price)


class Transaction(BasePayment):

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.SET_NULL)

    subscription_id = models.CharField(max_length=255, null=True, blank=True) # creating stripe subscription
    customer_id = models.CharField(max_length=255, null=True, blank=True) # for creating stripe subscription

    subscription_status = models.PositiveSmallIntegerField(choices=SUBSCRIPTION_STATUS.choices, default=SUBSCRIPTION_STATUS.INACTIVE)

    def get_failure_url(self) -> str:
        # Return a URL where users are redirected after
        # they fail to complete a payment:
        return reverse('payment-failed')

    def get_success_url(self) -> str:
        # Return a URL where users are redirected after
        # they successfully complete a payment:
        return reverse('payment-success')


    def get_purchased_items(self):
        # Return items that will be included in this payment.

        yield PurchasedItem(
            name=self.plan.name,
            sku='none',
            quantity=1,
            price=self.plan.price,
            currency='USD',
        )

    def get_total_dollars(self):
        # converts  cents to dollars.

        return cents_to_dollar(self.total)