# Generated by Django 4.1.5 on 2023-02-04 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_payment_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_setup',
            name='level',
            field=models.CharField(default='all', max_length=20),
        ),
    ]