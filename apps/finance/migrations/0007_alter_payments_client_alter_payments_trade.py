# Generated by Django 5.0 on 2024-04-03 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_payments_payment_type'),
        ('trade', '0005_trade_discount_summa_alter_tradedetail_trade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments_set', to='trade.client'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='trade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trade_set', to='trade.trade'),
        ),
    ]
