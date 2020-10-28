from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import CreateView

from recruiting import models
from recruiting.forms import SignUpForm


class MainView(View):
    def get(self, request):
        specialties = models.Specialty.objects.all()
        companies = models.Company.objects.all()
        return render(request, 'recruiting/index.html', context={
            'title': '',
            'specialties': specialties,
            'companies': companies
        })


class VacanciesView(View):
    def get(self, request):
        vacancies = models.Vacancy.objects.all()
        return render(request, 'recruiting/vacancies.html', context={
            'vacancies': vacancies,
            'title': 'Вакансии | ',
            'specialty_title': 'Все вакансии',
            'vacancies_count': vacancies.count()
        })


class VacanciesCatView(View):
    def get(self, request, category):
        specialty = get_object_or_404(models.Specialty, code=category)
        vacancies = models.Vacancy.objects.filter(specialty=specialty)
        return render(request, 'recruiting/vacancies.html', context={
            'title': specialty.title + ' | ',
            'specialty_title': specialty.title,
            'vacancies_count': vacancies.count,
            'vacancies': vacancies
        })


class CompaniesView(View):
    def get(self, request, company_id):
        company = get_object_or_404(models.Company, id=company_id)
        return render(request, 'recruiting/company.html', context={
            'title': company.name + ' | ',
            'company_logo': company.logo,
            'company_name': company.name,
            'company_vacancies_count': company.vacancies.count(),
            'company_vacancies': company.vacancies.all()
        })


class VacancyView(View):
    def get(self, request, vacancy_id):
        vacancy = get_object_or_404(models.Vacancy, id=vacancy_id)
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


class VacancySendView(View):
    pass


class MyCompanyView(View):
    pass


class MyCompanyVacanciesView(View):
    pass


class MyCompanyVacancyView(View):
    pass


class MySignupView(CreateView):
    form_class = SignUpForm
    success_url = '/login/'
    template_name = 'recruiting/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'recruiting/login.html'
