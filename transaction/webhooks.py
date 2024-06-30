import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from payments import PaymentStatus

from .models import Transaction, SUBSCRIPTION_STATUS

stripe.api_key = settings.PAYMENT_VARIANTS['stripe'][1]['secret_key']

STRIPE_WEBHOOK_SECRET = settings.PAYMENT_VARIANTS['stripe'][1]['endpoint_secret']

# https://docs.stripe.com/webhooks#local-listener

@require_POST
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'error': str(e)}, status=400)

    # print("Event: ", event)

    data = event['data']['object']

    # Handle the even
    if event['type'] == 'checkout.session.completed':
        subscription = Transaction.objects.get(transaction_id=data['id'])
        subscription.status = PaymentStatus.CONFIRMED
        subscription.subscription_status = SUBSCRIPTION_STATUS.ACTIVE
        subscription.subscription_id = data['subscription']
        subscription.customer_id = data['customer']
        subscription.save()

    if event['type'] == 'checkout.session.expired':
        subscription = Transaction.objects.get(transaction_id=data['id'])
        subscription.status = PaymentStatus.REJECTED
        subscription.save()

    elif event['type'] == 'customer.subscription.deleted':
        # Subscription deleted
        subscription = Transaction.objects.get(stripe_subscription_id=event['data']['object']['subscription'])
        subscription.subscription_status = SUBSCRIPTION_STATUS.CANCELLED
        subscription.save()

    elif event['type'] == "charge.failed":
        pass

    elif event['type'] == 'invoice.payment_succeeded':
        # Payment succeeded
        pass
    
    elif event['type'] == 'invoice.payment_failed':
        # Payment succeeded
        pass

    elif event['type'] == 'customer.subscription.trial_will_end':
        # print('Subscription trial will end')
        pass
    
    elif event['type'] == 'customer.subscription.created':
        # print('Subscription created %s', event.id)
        pass
    
    elif event['type'] == 'customer.subscription.updated':
        # print('Subscription created %s', event.id)
        pass

    return JsonResponse({'status': 'success'}, status=200)
