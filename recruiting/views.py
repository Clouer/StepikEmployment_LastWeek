from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from recruiting import models
from recruiting.forms import SignUpForm, ApplicationResponseForm, CreateCompanyForm, UpdateCompanyForm, \
    MyCompanyVacancyCreateForm, MyCompanyVacancyUpdateForm
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
            'form': UpdateCompanyForm,
            'title': title,
            'company': company
        })

    def post(self, request):
        form = UpdateCompanyForm(request.POST, request.FILES)
        company = request.user.owns
        if form.is_valid():
            cleaned_form = form.cleaned_data
            if cleaned_form.get('logo'):
                company.logo = cleaned_form['logo']
            company.name = cleaned_form['name']
            company.location = cleaned_form['location']
            company.description = cleaned_form['description']
            company.employee_count = cleaned_form['employee_count']
            company.save()
            messages.info(request, 'Информация о компании обновлена')
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
        got_vacancies = False
        if len(vacancies) > 0:
            got_vacancies = True
        return render(request, 'recruiting/vacancy-list.html', context={
            'vacancies': vacancies,
            'title': 'Вакансии компании |',
            'got_vacancies': got_vacancies,
        })


class CreateVacancyView(View):
    def get(self, request):
        return render(request, 'recruiting/vacancy-create.html', context={'form': MyCompanyVacancyCreateForm})

    def post(self, request):
        form = MyCompanyVacancyCreateForm(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            Vacancy.objects.create(
                title=cleaned_form['title'],
                specialty=cleaned_form['specialty'],
                company=request.user.owns,
                salary_min=cleaned_form['salary_min'],
                salary_max=cleaned_form['salary_max'],
                skills=cleaned_form['skills'],
                description=cleaned_form['description'],
                published_at=datetime.today().strftime('%Y-%m-%d')
            )
            return redirect(reverse('my_company_vacancies'))
        return HttpResponse(form.errors)
        # return render(request, 'recruiting/vacancy-create.html', context={'form': form})


class MyCompanyVacancyView(View):
    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        applications = ApplicationResponse.objects.filter(vacancy=vacancy)
        return render(request, 'recruiting/vacancy-edit.html', context={
            'form': MyCompanyVacancyCreateForm,
            'vacancy': vacancy,
            'title': 'Вакансии компании |',
            'applications': applications
        })

    def post(self, request, vacancy_id):
        form = MyCompanyVacancyCreateForm(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            vacancy = Vacancy.objects.get(id=vacancy_id)
            if cleaned_form.get('specialty'):
                vacancy.specialty = cleaned_form['specialty']
            vacancy.title = cleaned_form['title']
            vacancy.salary_min = cleaned_form['salary_min']
            vacancy.salary_max = cleaned_form['salary_max']
            vacancy.skills = cleaned_form['skills']
            vacancy.description = cleaned_form['description']
            vacancy.save()
            messages.info(request, 'Вакансия обновлена')
            return redirect(reverse('my_company_vacancy', kwargs={'vacancy_id': vacancy_id}))
        return redirect(reverse('my_company_vacancy', kwargs={
            'vacancy_id': vacancy_id
        }))


class MySignupView(CreateView):
    form_class = SignUpForm
    success_url = '/login/'
    template_name = 'recruiting/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'recruiting/login.html'
