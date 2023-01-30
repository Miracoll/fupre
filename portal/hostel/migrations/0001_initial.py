# Generated by Django 4.1.5 on 2023-01-28 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bedspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bedspace', models.CharField(max_length=255)),
                ('occupied', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('lock', models.BooleanField(default=False)),
                ('ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.CharField(max_length=10)),
                ('number_of_room', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('lock', models.BooleanField(default=False)),
                ('last_updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['hostel_id', 'created'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=50)),
                ('occupant_per_room', models.IntegerField(default=0)),
                ('available', models.BooleanField(default=True)),
                ('occupied', models.IntegerField(default=0)),
                ('space_available', models.IntegerField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('lock', models.BooleanField(default=False)),
                ('last_updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.floor')),
            ],
        ),
        migrations.CreateModel(
            name='Paid_Occupant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('occupant', models.CharField(max_length=255)),
                ('amount_paid', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('ref', models.CharField(max_length=200)),
                ('session', models.CharField(blank=True, max_length=10, null=True)),
                ('year', models.CharField(blank=True, max_length=5, null=True)),
                ('group', models.CharField(blank=True, max_length=5, null=True)),
                ('arm', models.CharField(blank=True, max_length=5, null=True)),
                ('status', models.IntegerField(default=1)),
                ('installment', models.IntegerField(blank=True, null=True)),
                ('hostel', models.CharField(max_length=255)),
                ('print', models.IntegerField(default=1)),
                ('paid_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Occupant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.CharField(max_length=255)),
                ('amount_paid', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=10)),
                ('session', models.CharField(max_length=100)),
                ('term', models.CharField(max_length=5)),
                ('ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('bedspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.bedspace')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostel_name', models.CharField(max_length=255)),
                ('floor_number', models.IntegerField()),
                ('image', models.ImageField(default='hostel.jpg', upload_to='hostel')),
                ('active', models.BooleanField(default=True)),
                ('lock', models.BooleanField(default=False)),
                ('ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='floor',
            name='hostel_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.hostel'),
        ),
        migrations.AddField(
            model_name='bedspace',
            name='floor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.floor'),
        ),
        migrations.AddField(
            model_name='bedspace',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.hostel'),
        ),
        migrations.AddField(
            model_name='bedspace',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.room'),
        ),
    ]