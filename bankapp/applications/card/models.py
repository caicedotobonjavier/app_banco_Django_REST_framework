from django.db import models
#
from model_utils.models import TimeStampedModel
#
import uuid
#
from applications.users.models import User
#
from applications.account.models import Account, TypeAccount
# Create your models here.


class Card(TimeStampedModel):
    card_id = models.UUIDField('Id Tarjeta', primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='card_user', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name='card_account', on_delete=models.CASCADE)
    type_account = models.ForeignKey(TypeAccount, related_name='card_typeaccount', on_delete=models.CASCADE)
    membership_date = models.DateField('Fecha Afiliacion')
    expiration_date = models.DateField('Fecha Expiracion')
    balance = models.IntegerField('Saldo')

    class Meta:
        verbose_name = 'Tarjeta'
        verbose_name_plural = 'Tarjetas'
    

    def __str__(self):
        return str(self.account.account_number)
