from django.db import models
#
from django.db.models import Sum, F



class TransactionManager(models.Manager):
    
    def transaction_date(self, **datos):
        transactions = self.filter(
            user = datos['user']
        ).filter(
            transaction_date__gt=datos['date1'],
            transaction_date__lte=datos['date2']
        )        
        
        return transactions
    

    def details_transactions(self, user):
        suma_retiros = self.filter(
            user=user
        ).filter(
            operation__description='Retiro'
        ).aggregate(
            total=Sum(F('transaction_amount'))
        )

        suma_consignaciones = self.filter(
            user=user
        ).filter(
            operation__description='Consignación'
        ).aggregate(
            total=Sum(F('transaction_amount'))
        )

        suma_transferencias = self.filter(
            user=user
        ).filter(
            operation__description='Transferencia'
        ).aggregate(
            total=Sum(F('transaction_amount'))
        )

        suma_pagosvirtuales = self.filter(
            user=user
        ).filter(
            operation__description='Pago Virtual'
        ).aggregate(
            total=Sum(F('transaction_amount'))
        )

        details ={
            'sum_retiros' : suma_retiros['total'],
            'sum_consignaciones' : suma_consignaciones['total'],
            'sum_transferencias' : suma_transferencias['total'],
            'sum_pagosvirtuales' : suma_pagosvirtuales['total']
        }
        

        return details

