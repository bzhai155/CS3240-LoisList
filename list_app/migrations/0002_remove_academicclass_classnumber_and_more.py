# Generated by Django 4.1.1 on 2022-11-05 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('list_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicclass',
            name='Classnumber',
        ),
        migrations.RemoveField(
            model_name='academicclass',
            name='code',
        ),
        migrations.RemoveField(
            model_name='academicclass',
            name='dates',
        ),
        migrations.RemoveField(
            model_name='academicclass',
            name='shopping',
        ),
        migrations.AddField(
            model_name='academicclass',
            name='catalog_number',
            field=models.CharField(blank=True, default='0000', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='class_capacity',
            field=models.IntegerField(blank=True, default='0'),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='component',
            field=models.CharField(blank=True, default='0000', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='course_number',
            field=models.IntegerField(blank=True, default='00000', primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='course_section',
            field=models.CharField(blank=True, default='0000', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='days',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='description',
            field=models.CharField(blank=True, default='0000', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='enrollment_available',
            field=models.IntegerField(blank=True, default='0'),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='enrollment_total',
            field=models.IntegerField(blank=True, default='0'),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='facility_description',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='instructor_email',
            field=models.EmailField(blank=True, default='D', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='instructor_name',
            field=models.CharField(blank=True, default='D', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='semester_code',
            field=models.CharField(blank=True, default='0000', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='subject',
            field=models.CharField(blank=True, default='0000', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='topic',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='units',
            field=models.CharField(blank=True, default='0000', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='wait_cap',
            field=models.IntegerField(blank=True, default='0'),
        ),
        migrations.AddField(
            model_name='academicclass',
            name='wait_list',
            field=models.IntegerField(blank=True, default='0'),
        ),
        migrations.AlterField(
            model_name='academicclass',
            name='end_time',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='academicclass',
            name='start_time',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.ManyToManyField(to='list_app.academicclass')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
