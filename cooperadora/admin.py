from django.contrib import admin
from .models import Transaction, CooperadoraProject


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'amount')
    list_filter = ('type', 'date')


@admin.register(CooperadoraProject)
class CooperadoraProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'budget')
