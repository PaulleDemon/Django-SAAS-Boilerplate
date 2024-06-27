from django.contrib import admin

from .models import Plan, Transaction

# Register your models here.
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):

    list_display = ['name', 'description', 'price']

    search_fields = ['name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = ['transaction_id', 'user', 'plan', 'status', 'total']

    search_fields = ['transaction_id']

    list_filter = ['status', 'created']