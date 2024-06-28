from django import forms
from payments import PaymentStatus


class PaymentForm(forms.Form):
    stripe_token = forms.CharField()
    plan_id = forms.CharField()
    
    def __init__(self, payment, *args, **kwargs):
        self.payment = payment
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        token = cleaned_data.get('stripe_token')
        if not token:
            raise forms.ValidationError('Missing Stripe token.')
        return cleaned_data

    def save(self):
        self.payment.change_status(PaymentStatus.WAITING)
        self.payment.attrs.token = self.cleaned_data['stripe_token']
        self.payment.save()
        self.payment.capture()


class StripeSubscriptionForm(forms.Form):
    stripe_token = forms.CharField()
    plan_id = forms.CharField()
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     token = cleaned_data.get('stripe_token')
    #     if not token:
    #         raise forms.ValidationError('Missing Stripe token.')
    #     return cleaned_data
