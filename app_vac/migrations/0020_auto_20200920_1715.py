# Generated by Django 3.1.1 on 2020-09-20 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_vac', '0019_applications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='applications',
            name='vacancy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications',
                                    to='app_vac.vacancy'),
        ),
    ]
