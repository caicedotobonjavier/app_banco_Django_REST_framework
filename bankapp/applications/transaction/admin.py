from django.contrib import admin
#
from .models import Transaction
# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'card',
        'account',
        'user',
        'operation',
        'transaction_date',
        'destination_account',
        'transaction_amount',
    )

    list_filter = (
        'transaction_date',
    )

admin.site.register(Transaction, TransactionAdmin)