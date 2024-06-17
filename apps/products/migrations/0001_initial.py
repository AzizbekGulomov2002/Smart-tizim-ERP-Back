# Generated by Django 5.0.4 on 2024-06-17 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.BigIntegerField(default=0)),
                ('name', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.BigIntegerField(default=0)),
                ('name', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.BigIntegerField(default=0)),
                ('name', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.BigIntegerField(default=0)),
                ('name', models.CharField(max_length=500)),
                ('supplier_type', models.CharField(choices=[('Tezkor', 'Tezkor'), ('Doimiy', 'Doimiy')], default='Tezkor', max_length=20)),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
                ('added', models.DateTimeField()),
                ('desc', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.BigIntegerField(default=0)),
                ('name', models.CharField(max_length=500)),
                ('product_type', models.CharField(choices=[('Sanaladigan', 'Sanaladigan'), ('Sanalmaydigan', 'Sanalmaydigan')], default='Sanaladigan', max_length=20)),
                ('price', models.PositiveIntegerField()),
                ('bar_code', models.TextField(blank=True, null=True)),
                ('deleted', models.DateField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.format')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StorageProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.BigIntegerField(default=0)),
                ('storage_type', models.CharField(choices=[('Naqtga', 'Naqtga'), ('Qarzga', 'Qarzga')], default='Naqtga', max_length=20)),
                ('size_type', models.CharField(choices=[("O'lchovli", "O'lchovli"), ("O'lchovsiz", "O'lchovsiz"), ('Formatli', 'Formatli')], default="O'lchovsiz", max_length=20)),
                ('storage_count', models.FloatField(default=1)),
                ('part_size', models.FloatField(blank=True, default=1, null=True)),
                ('height', models.FloatField(blank=True, default=1, null=True)),
                ('width', models.FloatField(blank=True, default=1, null=True)),
                ('price', models.FloatField(default=1)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('remind_count', models.FloatField(default=0, help_text='Eslatish miqdori ...')),
                ('expiration', models.DateField(blank=True, help_text='Yaroqlilik muddati ...', null=True)),
                ('deleted', models.DateField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storage_products', to='products.product')),
            ],
        ),
    ]
