# Generated by Django 5.0.4 on 2024-05-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_name', models.CharField(max_length=500)),
                ('first_name', models.CharField(max_length=200)),
                ('family_name', models.CharField(max_length=200)),
                ('phone', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('sum', models.IntegerField(default=0)),
            ],
        ),
    ]
