from django.contrib import admin


from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):

    list_display = ['email', 'name', 'inquiry_type', 'datetime']

    search_fields = ['email', 'id']

    list_filter = ['inquiry_type', 'datetime']

    # readonly_fields = ['name', 'email', 'phone', 'datetime',  'description']