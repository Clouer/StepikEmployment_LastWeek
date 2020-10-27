from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.CharField(max_length=150)
    description = models.CharField(max_length=400)
    employee_count = models.IntegerField()
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)


class Specialty(models.Model):
    code = models.SlugField(max_length=20)
    title = models.CharField(max_length=100)
    picture = models.CharField(max_length=150)


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=150)
    description = models.CharField(max_length=400)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()


class ApplicationResponse(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = models.CharField(max_length=12)
    written_cover_letter = models.CharField(max_length=300)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')