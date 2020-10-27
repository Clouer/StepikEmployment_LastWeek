from django.contrib import admin

from recruiting.models import Company, Vacancy, ApplicationResponse, Specialty


class CompanyAdmin(admin.ModelAdmin):
    pass


class VacancyAdmin(admin.ModelAdmin):
    pass


class ApplicationResponseAdmin(admin.ModelAdmin):
    pass


class SpecialityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(ApplicationResponse, ApplicationResponseAdmin)
admin.site.register(Specialty, SpecialityAdmin)
