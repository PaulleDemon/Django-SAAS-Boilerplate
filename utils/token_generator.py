import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mass_mail, send_mail

from .common import get_name_from_email


def create_verification_token(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=1),  # Set expiration time
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def send_token(email):
    """
        sends email token
    """

    token = create_verification_token(email)

    name = get_name_from_email(email)

    subject = f"Email confirmation link"
    message = f"""Hi {name},\nThanks for signing up. Follow the link to confirm your email {settings.DOMAIN}/user/email/verify/?token={token} \n\nregards, {settings.PROJECT_TITLE} Team"""

    send_mail(subject, message, from_email=None, recipient_list=[email])

