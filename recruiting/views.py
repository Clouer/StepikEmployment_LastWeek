from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from recruiting import models
from recruiting.forms import SignUpForm, ApplicationResponseForm, CreateCompanyForm
from recruiting.models import ApplicationResponse, Vacancy, Company


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
            'company': company.id,
            'form': ApplicationResponseForm,
        })

    def post(self, request, vacancy_id):
        form = ApplicationResponseForm(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            ApplicationResponse.objects.create(
                written_username=cleaned_form['written_username'],
                written_phone=cleaned_form['written_phone'],
                written_cover_letter=cleaned_form['written_cover_letter'],
                vacancy=Vacancy.objects.get(id=vacancy_id),
                user=request.user
            )
            return redirect(reverse('send_vacancy', kwargs={'vacancy_id': vacancy_id}))
        return redirect(reverse('vacancy', kwargs={'vacancy_id': vacancy_id}))


class VacancySendView(View):
    def get(self, request, vacancy_id):
        return render(request, 'recruiting/sent.html', context={'vacancy_id': vacancy_id})


class MyCompanyView(View):
    def get(self, request):
        company = ''
        try:
            request.user.owns
            template = 'recruiting/company-edit.html'
            title = 'Моя компания |'
            company = request.user.owns
        except User.owns.RelatedObjectDoesNotExist:
            template = 'recruiting/company-create.html'
            title = 'Создать карточку компании |'
        return render(request, template, context={
            'form': CreateCompanyForm,
            'title': title,
            'company': company
        })

    def post(self, request):
        form = CreateCompanyForm(request.POST, request.FILES)
        company = request.user.owns
        if form.is_valid():
            cleaned_form = form.cleaned_data
            company.name = cleaned_form['name']
            company.location = cleaned_form['location']
            company.logo = cleaned_form['logo']
            company.description = cleaned_form['description']
            company.employee_count = cleaned_form['employee_count']
            company.save()
            return redirect(reverse('my_company'))
        return HttpResponse(form.errors)


class CreateCompanyView(View):
    def get(self, request):
        return render(request, 'recruiting/company-create-form.html', context={'form': CreateCompanyForm})

    def post(self, request):
        form = CreateCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            Company.objects.create(
                name=cleaned_form['name'],
                location=cleaned_form['location'],
                logo=cleaned_form['logo'],
                description=cleaned_form['description'],
                employee_count=cleaned_form['employee_count'],
                owner=request.user
            )
            return redirect(reverse('my_company'))
        return render(request, 'recruiting/company-create-form.html', context={'form': form})


class MyCompanyVacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.filter(company=request.user.owns)
        return render(request, 'recruiting/vacancy-list.html', context={
            'vacancies': vacancies,
            'title': 'Вакансии компании |'
        })


class MyCompanyVacancyView(View):
    pass


# Вакансии компании |


class MySignupView(CreateView):
    form_class = SignUpForm
    success_url = '/login/'
    template_name = 'recruiting/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'recruiting/login.html'
