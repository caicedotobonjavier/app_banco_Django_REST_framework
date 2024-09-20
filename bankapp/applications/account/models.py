from django.db import models
#
from model_utils.models import TimeStampedModel
#
from applications.users.models import User
#
import uuid
# Create your models here.

class Account(TimeStampedModel):
    account_id = models.UUIDField('Id Cuenta', default=uuid.uuid4, editable=False)
    account_number = models.CharField('Numero Cuenta', primary_key=True, max_length=10, unique=True)
    user_id = models.ForeignKey(User, related_name='account_user', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ['-created']

    def __str__(self):
        return self.account_number



class TypeAccount(TimeStampedModel):

    AHORROS = '1'
    CORRIENTE = '2'
    NOMINA = '3'
    PENSION = '4'
    INFANTIL = '5'
    JOVEN = '6'


    TIPO_CUENTA_CHOICES = [
        (AHORROS, 'Ahorros'),
        (CORRIENTE, 'Corriente'),
        (NOMINA, 'Nomina'),
        (PENSION, 'Pension'),
        (INFANTIL, 'Infantil'),
        (JOVEN, 'Joven')
    ]
    
    account = models.ForeignKey(Account, related_name='type_account', on_delete=models.CASCADE)
    account_type = models.CharField('Descripcion', max_length=1, choices=TIPO_CUENTA_CHOICES, default=AHORROS)

    class Meta:
        verbose_name = 'Tipo Cuenta'
        verbose_name_plural = 'Tipos Cuenta'
        ordering = ['-created']
        unique_together = ('account', 'account_type')
    

    def __str__(self):
        return self.get_account_type_display()