from django.urls import path

from .views import inquiry_view, inquiry_api_view, inquiry_success


urlpatterns = [
    path('', inquiry_view, name='contact-us'),
    path('success/', inquiry_success, name='contact-success'),
    path('api/', inquiry_api_view, name='contact_api_view')
]
