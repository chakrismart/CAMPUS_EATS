# Generated by Django 5.1.5 on 2025-02-14 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_customer_profile_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
    ]
