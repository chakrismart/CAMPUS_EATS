# Generated by Django 5.1.5 on 2025-02-11 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='username',
            field=models.CharField(default='user', max_length=50, unique=True),
        ),
    ]
