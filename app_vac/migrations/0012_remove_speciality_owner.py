# Generated by Django 3.1.1 on 2020-09-18 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_vac', '0011_speciality_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speciality',
            name='owner',
        ),
    ]
