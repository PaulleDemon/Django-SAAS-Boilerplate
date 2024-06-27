import jwt
import json

from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods


from .models import User
from .forms import CustomUserCreationForm
from utils.token_generator import send_token


def o_auth_login(request):

    return render(request, 'oAuth-login.html')


# class CustomLoginView(LoginView):
#     template_name = 'oAuth-login.html' 

def login_view(request):
    next_url = request.GET.get('next', '')

    if request.user.is_authenticated:
        if next_url and next_url != request.path:
            return redirect(next_url)
        
        return redirect('home')

    if request.method == "GET":
        return render(request, 'login.html')

    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(request, username=email, password=password)
    
    if User.objects.filter(email=email, is_active=False).exists():
        url = reverse('verification-alert') + f'?email={email}'
        
        return redirect(url)

    if user is not None:
        login(request, user)
                
        if next_url and next_url != request.path:
            return redirect(next_url)
        
        return redirect('home')

    return render(request, 'login.html', {'error': f'Invalid email or password'})


def logout_view(request):
    logout(request)

    return redirect('home')


@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    
    else:   
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            # login(request, user) # don't login user unless the user has verified their email
            send_token(username)

            url = reverse('verification-alert') + f'?email={username}'
            return redirect(url)

        error = form.errors.as_data()

        errors = [f'{list(error[x][0])[0]}' for x in error]
       
        return render(request, 'signup.html', context={'errors': errors})


def verification_alert(request):
    """
        alert that the user has to verify their email
    """
    email = request.GET.get('email') or ''
    return render(request, 'verification-alert.html', context={'from_email': settings.EMAIL_HOST,
                                                                'to_email': email   
                                                            })


@require_http_methods(["GET", "POST"])
def verification_resend(request):
    """
        resend the confirmation email
    """

    if request.method == "POST":

        email = request.POST.get('email')

        user = User.objects.filter(email=email)

        if not user.exists():

            return render(request, 'resend-confirmation.html', {'error': f'The email {email} is not registered'})

        if user.filter(is_active=True):
            return render(request, 'resend-confirmation.html', {'error': f'The email {email} is already active'})

        send_token(email)
        url = reverse('verification-alert') + f'?email={email}'
        return redirect(url)

    return render(request, 'resend-confirmation.html')


def verify_email(request):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        email = payload['email']

        user = get_user_model().objects.get(email=email)
        user.is_active = True
        user.save()

        send_token(email)

        return redirect('login')  # Redirect to a success page

    except jwt.ExpiredSignatureError:
        return render(request, 'email-verification.html', context={'error': 'Token expired, request another'})

    except (jwt.DecodeError, Exception):
        return render(request, 'email-verification.html', context={'error': 'Unknown error occurred, request a new token'})