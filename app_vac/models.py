from django.contrib.auth.models import User
from django.db import models

from vacancies.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, null=True)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company', null=True)
    location = models.CharField(max_length=64, null=True)

    class Meta:
        app_label = 'app_vac'


class Speciality(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.TextField()
    name = models.CharField(max_length=64)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    class Meta:
        app_label = 'app_vac'


class Vacancy(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()

    class Meta:
        app_label = 'app_vac'


class Applications(models.Model):
    written_username = models.CharField(max_length=128)
    written_phone = models.CharField(max_length=16)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', null=True)

    class Meta:
        app_label = 'app_vac'
