# Generated by Django 4.1.1 on 2022-11-14 23:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('list_app', '0009_calender'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Calender',
            new_name='CalenderModel',
        ),
    ]
