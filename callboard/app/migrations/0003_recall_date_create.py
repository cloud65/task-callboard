# Generated by Django 4.1.1 on 2022-09-20 04:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_emailcodes'),
    ]

    operations = [
        migrations.AddField(
            model_name='recall',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
