from django.contrib import admin
#
from .models import Account, TypeAccount
# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'account_id',
        'account_number',
        'user_id',
    )


admin.site.register(Account, AccountAdmin)



class TypeAccountAdmin(admin.ModelAdmin):
    list_display = (
        'account',
        'account_type',
    )


admin.site.register(TypeAccount, TypeAccountAdmin)
