import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'conf.settings'
django.setup()  # Всякие Django штуки импортим после сетапа


from recruiting import data, models


if __name__ == '__main__':
    for cat in data.specialties:
        specialty_data = models.Specialty.objects.create(
            code=cat['code'],
            title=cat['title'],
            picture=cat['picture']
        )

    for company in data.companies:
        company_data = models.Company.objects.create(
            name=company['name'],
            location=company['location'],
            logo=company['logo'],
            description=company['description'],
            employee_count=company['employee_count']
        )

    for job in data.vacancies:
        job_data = models.Vacancy.objects.create(
            title=job['title'],
            specialty=models.Specialty.objects.get(code=job['specialty']),
            company=models.Company.objects.get(name=job['company']),
            skills=job['skills'],
            description=job['description'],
            salary_min=job['salary_min'],
            salary_max=job['salary_max'],
            published_at=job['published_at']
        )
