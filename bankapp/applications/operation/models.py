from django.db import models
#
from model_utils.models import TimeStampedModel
# Create your models here.


class Operation(TimeStampedModel):
    description = models.CharField('Descripcion', max_length=50)

    class Meta:
        verbose_name = 'Operacion'
        verbose_name_plural = 'Operaciones'
        ordering = ['created']

    def __str__(self):
        return self.description