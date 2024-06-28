import stripe
from django.shortcuts import render
from django.conf import settings

from django.views.generic import View
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from payments import get_payment_model, RedirectNeeded

from .models import Plan, Transaction
from .forms import StripeSubscriptionForm

Payment = get_payment_model()
stripe.api_key = settings.PAYMENT_VARIANTS['stripe'][1]['secret_key']


@login_required
@require_http_methods(['POST'])
def create_payment(request):

    plan = request.POST.get("plan")

    try:
        plan = Plan.objects.get(id=int(plan))
    
    except (Plan.DoesNotExist, ValueError):
        return render(request, "404.html", status=404)

    amount = plan.price 
    currency = 'usd'

    payment = Payment.objects.create(
        variant='stripe',  # This is the key in PAYMENT_VARIANTS
        total=amount,
        currency=currency,
        description=plan.description  or '',
        billing_email=request.user.email,
        user=request.user,
        plan=plan
    )

    pay_data = {
                'price_data' :{
                        'product_data': {
                            'name': f'{plan.name}',
                            'description': plan.description or '',
                            },
                        'unit_amount': plan.get_total_cents(),
                        'currency': currency,
                        'recurring': {'interval': 'month'} # refer: https ://docs.stripe.com/api/checkout/sessions/create?lang=cli#create_checkout_session-line_items-price_data-recurring
                    },
                'quantity' : 1
            }


    checkout_session = stripe.checkout.Session.create(
            line_items=[
                pay_data
            ],
            mode='subscription',
            success_url=request.build_absolute_uri(payment.get_success_url()),
            cancel_url=request.build_absolute_uri(payment.get_failure_url()),
            customer=None,
            client_reference_id=request.user.id,
            customer_email=request.user.email,
            metadata={
                'customer': request.user.id,
                'payment_id': payment.id
            }
        )
    
    payment.transaction_id = checkout_session.id
    payment.save()

    return redirect(checkout_session.url)


# @login_required
# def payment_details(request, payment_id):
#     payment = get_object_or_404(get_payment_model(), id=payment_id)
    
#     try:
#         form = payment.get_form(data=request.POST or None)
#     except RedirectNeeded as redirect_to:
#         return redirect(str(redirect_to))

#     return TemplateResponse(
#         request,
#         'html/payment/stripe.html',
#         {'form': form, 'payment': payment}
#     )


def pricing(request):

    plans = Plan.objects.all()

    return render(request, "payment/pricing.html", {
        'plans': plans
    })


def payment_success(request):

    return render(request, "html/payment/success.html")


def payment_failed(request):

    return render(request, "html/payment/failure.html")