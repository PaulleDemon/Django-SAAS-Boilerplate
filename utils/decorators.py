from functools import wraps

from django.conf import settings  # Import the Django settings module
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe


def login_required_for_post(function, login_url=settings.LOGIN_URL):
    
    def wrapper_func(request, *args, **kwargs):
        if request.method == 'POST' and not request.user.is_authenticated:
            return redirect(login_url)

        return function(request, *args, **kwargs)

    return wrapper_func


def login_required_rest_api(function, login_url=settings.LOGIN_URL):

    def wrapper_func(request, *args, **kwargs):
        if  not request.user.is_authenticated:
            return JsonResponse({'redirect': login_url}, status=302)

        return function(request, *args, **kwargs)

    return wrapper_func
