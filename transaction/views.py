from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from payments import get_payment_model, RedirectNeeded

from utils.money import dollar_to_cents

from .models import Plan

Payment = get_payment_model()


@login_required
@require_http_methods(['POST'])
def create_payment(request):

    plan = request.POST.get("plan")

    try:
        plan = Plan.objects.get(id=int(plan))
    
    except (Plan.DoesNotExist, ValueError):
        return render(request, "404.html", status=404)

    amount = dollar_to_cents(plan.price)  # Amount in cents
    currency = 'usd'

    payment = Payment.objects.create(
        variant='stripe',  # This is the key in PAYMENT_VARIANTS
        total=amount,
        currency=currency,
        description=plan.description  or '',
        billing_email=request.user.email,
        user=request.user
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