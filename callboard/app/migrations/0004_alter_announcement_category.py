# Generated by Django 4.1.1 on 2022-09-21 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_recall_date_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='announcements', to='app.category'),
        ),
    ]