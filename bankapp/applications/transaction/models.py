from django.db import models
#
from model_utils.models import TimeStampedModel
#
import uuid
#
from applications.card.models import Card
#
from applications.account.models import Account
#
from applications.users.models import User
#
from applications.operation.models import Operation
#
from .managers import TransactionManager
# Create your models here.


class Transaction(TimeStampedModel):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='transactions_card')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_account')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_user')
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='transactions_operation')
    transaction_date = models.DateTimeField('Fecha Transacion')
    destination_account = models.CharField('Cuenta Destino', max_length=100)
    transaction_amount = models.IntegerField('Monto de Transaccion')

    objects = TransactionManager()


    class Meta:
        verbose_name = 'Transaccion'
        verbose_name_plural = 'Transacciones'
    

    def __str__(self):
        return str(self.transaction_id)

