# Generated by Django 5.0.4 on 2024-04-03 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.supplier'),
        ),
    ]
