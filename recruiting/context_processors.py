from recruiting import models


def data_models(request):
    vacancies = models.Vacancy.objects.all()
    companies = models.Company.objects.all()
    specialties = models.Specialty.objects.all()

    return {
        'vacancies': vacancies,
        'specialties': specialties,
        'companies': companies
    }
