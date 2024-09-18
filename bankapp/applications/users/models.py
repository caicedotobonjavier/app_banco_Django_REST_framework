from django.db import models
#
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#
from .managers import UserManager
#
from .functions import create_cod
#
from django.db.models.signals import post_save
#
from django.dispatch import receiver
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', max_length=254, unique=True)
    full_name = models.CharField('Nombre Completo', max_length=150)
    date_birth = models.DateField('Fecha nacimiento', null=True, blank=True)
    phone = models.CharField('Telefono', max_length=15, null=True, blank=True)
    address = models.CharField('Direccion', max_length=50, null=True, blank=True)
    activation_code = models.CharField('Codigo de activacion', max_length=6, null=True, blank=True)
    #
    #validation otp
    otp_base32 = models.CharField('OTP 32', max_length=255, null=True, blank=True)
    login_otp = models.CharField('OTP Login', max_length=255, null=True, blank=True)
    user_login_otp = models.BooleanField('Login Usado', default=False)
    created_at = models.DateField('OTP Creado', null=True, blank=True)
    #
    
    is_active = models.BooleanField('Activo', default=False)
    is_staff = models.BooleanField('Usuario', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


    def get_email(self):
        return self.email

    def get_full_name(self):
        return self.full_name
    

#cuando se crea un usurio automaticamente se crea el codigo de registro
@receiver(post_save, sender=User)
def set_activation_code(sender, instance, created, **kwargs):
    if created:
        instance.activation_code = create_cod()
        instance.save()