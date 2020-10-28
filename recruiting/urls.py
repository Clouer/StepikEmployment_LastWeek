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
]
