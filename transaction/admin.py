from typing import Any
from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Plan, Transaction

@admin.register(Plan)
class PlanAdmin(ModelAdmin):

    list_display = ['name', 'description', 'price']

    search_fields = ['name']

    def get_form(self, request: Any, *args, **kwargs) -> Any:
        form = super().get_form(request, *args, **kwargs)

        if "features" in form.base_fields:
            form.base_fields["features"].help_text = "Separate features with a comma (eg: feature1, feature2)"


        return form

@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):

    list_display = ['id', 'transaction_id', 'user', 'plan', 'status', 'created', 'total']

    search_fields = ['transaction_id', 'user__email']

    list_filter = ['plan', 'status', 'created']

    readonly_fields = ['created', 'modified']

    # def get_total(self, obj):
    #     return f'${obj.get_total_dollars()}'
    
    # get_total.short_description = 'total'