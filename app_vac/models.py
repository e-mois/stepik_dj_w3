from django.db import models

# Create your models here.


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    logo = models.TextField()
    description = models.TextField()
    employee_count = models.IntegerField()

    class Meta:
        app_label = 'app_vac'


class Speciality(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.TextField()
    name = models.CharField(max_length=64)
    picture = models.TextField()

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
