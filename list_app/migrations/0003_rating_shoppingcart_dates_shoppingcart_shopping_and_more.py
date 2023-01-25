# Generated by Django 4.1.1 on 2022-11-06 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_app', '0002_remove_academicclass_classnumber_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='dates',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='shopping',
            field=models.ManyToManyField(to='list_app.student'),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='ratings',
            field=models.ManyToManyField(to='list_app.rating'),
        ),
    ]