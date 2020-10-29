from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from recruiting.models import ApplicationResponse, Company


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']


class ApplicationResponseForm(forms.ModelForm):
    class Meta:
        model = ApplicationResponse
        fields = ['written_username', 'written_phone', 'written_cover_letter']


class CreateCompanyForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Company
        fields = ['name', 'location', 'logo', 'description', 'employee_count']
