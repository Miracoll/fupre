# Generated by Django 4.1.5 on 2023-01-16 19:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_remove_payment_setup_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.CharField(max_length=100)),
                ('rrr', models.CharField(max_length=20)),
                ('status', models.BooleanField(default=False)),
                ('order_id', models.CharField(max_length=1000)),
                ('ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('generated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('paid_on', models.DateTimeField(blank=True, null=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.payment_setup')),
            ],
        ),
    ]
