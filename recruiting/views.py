from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from recruiting import models
from recruiting.forms import SignUpForm, ApplicationResponseForm, CreateCompanyForm, UpdateCompanyForm, \
    MyCompanyVacancyCreateForm, CreateResumeForm, SearchForm
from recruiting.models import ApplicationResponse, Vacancy, Company, Resume


class MainView(View):
    def get(self, request):
        specialties = models.Specialty.objects.all()
        companies = models.Company.objects.all()
        return render(request, 'recruiting/index.html', context={
            'title': '',
            'specialties': specialties,
            'companies': companies,
            'form': SearchForm
        })

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            search_request = cleaned_form['search_request']
            return redirect(reverse('search', kwargs={'search_request': search_request}))
        return redirect(reverse('main'))


class SearchView(View):
    def get(self, request, search_request):
        search_result = Vacancy.objects.all().filter(title__icontains=search_request) | Vacancy.objects.all().filter(
            description__icontains=search_request)
        return render(request, 'recruiting/search.html', context={
            'title': 'Результат поиска | ',
            'search_result': search_result,
            'search': search_request,
            'form': SearchForm
        })

    def post(self, request, search_request):
        form = SearchForm(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            search_request = cleaned_form['search_request']
            return redirect(reverse('search', kwargs={'search_request': search_request}))
        return redirect(reverse('main'))


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
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
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
        messages.info(request, 'Введите корректные данные')
        return redirect(reverse('my_company'))


class CreateCompanyView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
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
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
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
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return render(request, 'recruiting/vacancy-create.html', context={'form': MyCompanyVacancyCreateForm})

    def post(self, request):
        form = MyCompanyVacancyCreateForm(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            if cleaned_form['specialty'] is None:
                messages.error(request, 'Введите корректные данные')
                return render(request, 'recruiting/vacancy-create.html', context={'form': form})
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
        return render(request, 'recruiting/vacancy-create.html', context={'form': form})


class MyCompanyVacancyView(View):
    def get(self, request, vacancy_id):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        if Vacancy.objects.get(id=vacancy_id).company != request.user.owns:
            return redirect(reverse('my_company_vacancies'))
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
        return render(request, 'recruiting/vacancy-create.html', context={'form': form})


class ResumeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        error_alert = True
        resume = ''
        try:
            request.user.resume
            template = 'recruiting/resume-edit.html'
            resume = request.user.resume
        except User.resume.RelatedObjectDoesNotExist:
            template = 'recruiting/resume-create.html'
        return render(request, template, context={
            'title': 'Моё резюме |',
            'form': CreateResumeForm,
            'resume': resume,
            'error_alert': error_alert
        })

    def post(self, request):
        form = CreateResumeForm(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            resume = request.user.resume
            if cleaned_form['status'] != '':
                resume.status = cleaned_form['status']
            if cleaned_form['grade'] != '':
                resume.grade = cleaned_form['grade']
            if cleaned_form['specialty']:
                resume.specialty = cleaned_form['specialty']
            resume.portfolio = cleaned_form['portfolio']
            resume.first_name = cleaned_form['first_name']
            resume.last_name = cleaned_form['last_name']
            resume.salary = cleaned_form['salary']
            resume.education = cleaned_form['education']
            resume.experience = cleaned_form['experience']
            resume.save()
            messages.info(request, 'Ваше резюме обновлено!')
            return redirect(reverse('my_resume'))
        messages.error(request, 'Введённые данные некорректны')
        return redirect(reverse('my_resume'))


class CreateResumeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        error_alert = False
        return render(request, 'recruiting/resume-edit.html', context={
            'title': 'Создать резюме |',
            'form': CreateResumeForm,
            'error_alert': error_alert
        })

    def post(self, request):
        form = CreateResumeForm(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            try:
                if cleaned_form['status'] == '' or cleaned_form['grade'] == '':
                    raise IntegrityError
                Resume.objects.create(
                    user=request.user,
                    first_name=cleaned_form['first_name'],
                    last_name=cleaned_form['last_name'],
                    status=cleaned_form['status'],
                    specialty=cleaned_form['specialty'],
                    salary=cleaned_form['salary'],
                    grade=cleaned_form['grade'],
                    education=cleaned_form['education'],
                    experience=cleaned_form['experience'],
                    portfolio=cleaned_form['portfolio']
                )
                messages.info(request, 'Ваше резюме создано!')
                return redirect(reverse('my_resume'))
            except IntegrityError:
                messages.error(request, 'Введите корректные данные!')
                return redirect(reverse('create_resume'))
        return render(request, 'recruiting/resume-edit.html', context={'form': form})


class MySignupView(CreateView):
    form_class = SignUpForm
    success_url = '/login/'
    template_name = 'recruiting/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'recruiting/login.html'
