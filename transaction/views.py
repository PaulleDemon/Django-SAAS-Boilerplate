from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from payments import get_payment_model, RedirectNeeded

from .models import Plan

Payment = get_payment_model()


@login_required
@require_http_methods(['POST'])
def create_payment(request):

    # Assuming you have some way of determining the amount and currency
    amount = 5000  # Amount in cents
    currency = 'usd'

    payment = Payment.objects.create(
        variant='stripe',  # This is the key in PAYMENT_VARIANTS
        total=amount,
        currency=currency,
        description='Payment description',
        billing_first_name='John',
        billing_last_name='Doe',
        billing_address_1='123 Street',
        billing_address_2='',
        billing_city='City',
        billing_postcode='12345',
        billing_country_code='US',
        billing_email='customer@example.com'
    )

    return redirect('payment', payment_id=payment.id)



def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)

    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

    return TemplateResponse(
        request,
        'payment.html',
        {'form': form, 'payment': payment}
    )


def pricing(request):

    plans = Plan.objects.all()

    return render(request, "payment/pricing.html", {
        'plans': plans
    })