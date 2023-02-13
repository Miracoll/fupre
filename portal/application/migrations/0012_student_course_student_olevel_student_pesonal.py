# Generated by Django 4.1.5 on 2023-02-13 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_olevel_sub52'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.course'),
        ),
        migrations.AddField(
            model_name='student',
            name='olevel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.olevel'),
        ),
        migrations.AddField(
            model_name='student',
            name='pesonal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.personal'),
        ),
    ]