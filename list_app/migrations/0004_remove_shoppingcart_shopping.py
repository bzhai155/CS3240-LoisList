# Generated by Django 4.1.1 on 2022-11-07 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list_app', '0003_rating_shoppingcart_dates_shoppingcart_shopping_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='shopping',
        ),
    ]
