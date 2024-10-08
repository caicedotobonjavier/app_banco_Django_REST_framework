# Generated by Django 5.1.1 on 2024-09-20 16:28

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('card_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id Tarjeta')),
                ('membership_date', models.DateField(verbose_name='Fecha Afiliacion')),
                ('expiration_date', models.DateField(verbose_name='Fecha Expiracion')),
                ('balance', models.IntegerField(verbose_name='Saldo')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_account', to='account.account')),
                ('type_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_typeaccount', to='account.typeaccount')),
            ],
            options={
                'verbose_name': 'Tarjeta',
                'verbose_name_plural': 'Tarjetas',
            },
        ),
    ]
