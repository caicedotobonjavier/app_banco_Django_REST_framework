from django.contrib import admin
#
from .models import Card
# Register your models here.

class CardAdmin(admin.ModelAdmin):
    list_display = (
        'card_id', 
        'user', 
        'account', 
        'balance',
        'type_account', 
        'membership_date', 
        'expiration_date',
    ) 

admin.site.register(Card, CardAdmin)