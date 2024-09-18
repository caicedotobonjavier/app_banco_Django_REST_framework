from django.contrib import admin
#
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'full_name',
        'date_birth',
        'phone',
        'address',
        'is_active',
        'is_staff',
        'is_superuser',
    )


admin.site.register(User, UserAdmin)