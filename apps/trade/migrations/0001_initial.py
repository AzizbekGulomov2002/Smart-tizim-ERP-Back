# Generated by Django 5.0.4 on 2024-05-23 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.BigIntegerField(default=0)),
                ('client_type', models.CharField(choices=[('Tezkor', 'Tezkor'), ('Doimiy', 'Doimiy')], default='Tezkor', max_length=20)),
                ('name', models.CharField(max_length=400)),
                ('phone', models.CharField(max_length=13)),
                ('added', models.DateTimeField()),
                ('desc', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('debt', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.BigIntegerField(default=0)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Addition_service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.BigIntegerField(default=0)),
                ('service_price', models.PositiveBigIntegerField()),
                ('service_date', models.DateTimeField()),
                ('desc', models.TextField(blank=True, null=True)),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addition_service', to='trade.servicetype')),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.BigIntegerField(default=0)),
                ('trade_type', models.CharField(choices=[('Naqtga', 'Naqtga'), ('Qarzga', 'Qarzga')], default='Naqtga', max_length=20)),
                ('discount_type', models.CharField(choices=[("Narx bo'yicha chegirma", "Narx bo'yicha chegirma"), ('Umumiy savdodan chegirma', 'Umumiy savdodan chegirma')], default='Umumiy savdodan chegirma', max_length=24, null=True)),
                ('discount_summa', models.FloatField(default=0)),
                ('trade_date', models.DateTimeField(blank=True, null=True)),
                ('check_id', models.IntegerField(blank=True, default=10000, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.client')),
            ],
        ),
    ]
