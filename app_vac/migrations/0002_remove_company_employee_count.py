# Generated by Django 3.1.1 on 2020-09-12 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_vac', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='employee_count',
        ),
    ]
