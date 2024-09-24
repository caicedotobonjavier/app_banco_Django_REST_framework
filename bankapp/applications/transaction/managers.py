from django.db import models
#



class TransactionManager(models.Manager):
    
    def transaction_date(self, **datos):
        transactions = self.filter(
            user = datos['user']
        ).filter(
            transaction_date__gt=datos['date1'],
            transaction_date__lte=datos['date2']
        )        
        
        return transactions
