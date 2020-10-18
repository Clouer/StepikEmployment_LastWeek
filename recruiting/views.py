from django.shortcuts import render
from django.views import View
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from recruiting import models


class MainView(View):
    def get(self, request):
        return render(request, 'recruiting/index.html', context={'title': ''})


class VacanciesView(View):
    def get(self, request):
        vacancies = models.Vacancy.objects.all()
        return render(request, 'recruiting/vacancies.html', context={
            'title': 'Вакансии | ',
            'vacancies_title': 'Все вакансии',
            'vacancies_count': vacancies.count()
        })


class VacanciesCatView(View):
    def get(self, request, category):
        try:
            specialty = models.Specialty.objects.get(code=category)
        except ObjectDoesNotExist:
            raise Http404
        vacancies = models.Vacancy.objects.filter(specialty=specialty)
        return render(request, 'recruiting/vacancies.html', context={
            'title': specialty.title + ' | ',
            'specialty_title': specialty.title,
            'vacancies_count': vacancies.count,
            'vacancies': vacancies
        })


class CompaniesView(View):
    def get(self, request, company_id):
        try:
            company = models.Company.objects.get(id=company_id)
        except ObjectDoesNotExist:
            raise Http404
        return render(request, 'recruiting/company.html', context={
            'title': company.name + ' | ',
            'company_logo': company.logo,
            'company_name': company.name,
            'company_vacancies_count': company.vacancies.count(),
            'company_vacancies': company.vacancies.all()
        })


class VacancyView(View):
    def get(self, request, vacancy_id):
        try:
            vacancy = models.Vacancy.objects.get(id=vacancy_id)
        except ObjectDoesNotExist:
            raise Http404
        company = vacancy.company
        return render(request, 'recruiting/vacancy.html', context={
            'title': vacancy.title + ' | ',
            'company_logo': vacancy.company.logo,
            'vacancy_title': vacancy.title,
            'vacancy_min': vacancy.salary_min,
            'vacancy_max': vacancy.salary_max,
            'vacancy_skills': vacancy.skills,
            'vacancy_description': vacancy.description,
            'company': company.id
        })
