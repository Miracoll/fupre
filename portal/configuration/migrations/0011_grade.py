# Generated by Django 4.1.5 on 2023-01-30 03:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0010_department_number_of_years'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=5)),
                ('description', models.CharField(max_length=20)),
                ('max_score', models.IntegerField()),
                ('min_score', models.IntegerField()),
                ('point', models.IntegerField()),
                ('ref', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
    ]
