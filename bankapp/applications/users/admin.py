from django.contrib import admin
#
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'email',
        'full_name',
        'activation_code',
        'otp_base32',
        'login_otp',
        'user_login_otp',
        'is_active',
        'is_staff',
        'is_superuser',
    )


admin.site.register(User, UserAdmin)