from django.urls import path
from django.contrib.auth.views import LogoutView

from recruiting import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.MySignupView.as_view(), name='signup'),
    path('vacancies/', views.VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:category>/', views.VacanciesCatView.as_view(), name='vacancies_cat'),
    path('companies/<int:company_id>/', views.CompaniesView.as_view(), name='company'),
    path('vacancies/<int:vacancy_id>/', views.VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_id>/send/', views.VacancySendView.as_view(), name='send_vacancy'),
    path('mycompany/', views.MyCompanyView.as_view(), name='my_company'),
    path('mycompany/create/', views.CreateCompanyView.as_view(), name='create_company'),
    path('mycompany/vacancies/', views.MyCompanyVacanciesView.as_view(), name='my_company_vacancies'),
    path('mycompany/vacancies/create/', views.CreateVacancyView.as_view(), name='create_vacancy'),
    path('mycompany/vacancies/<int:vacancy_id>/', views.MyCompanyVacancyView.as_view(), name='my_company_vacancy'),
    path('myresume/', views.ResumeView.as_view(), name='my_resume'),
    path('myresume/create/', views.CreateResumeView.as_view(), name='create_resume'),
    path('search?s=<str:search_request>/', views.SearchView.as_view(), name='search')


]
