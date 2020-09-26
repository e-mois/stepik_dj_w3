# Generated by Django 3.1.1 on 2020-09-18 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_vac', '0006_auto_20200919_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
