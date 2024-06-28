from django.contrib import admin

from .models import Plan, Transaction


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):

    list_display = ['name', 'description', 'price']

    search_fields = ['name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = ['id', 'transaction_id', 'user', 'plan', 'status', 'total']

    search_fields = ['transaction_id', 'user__email']

    list_filter = ['plan', 'status', 'created']

    # def get_total(self, obj):
    #     return f'${obj.get_total_dollars()}'
    
    # get_total.short_description = 'total'