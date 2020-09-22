from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.views.generic import CreateView

from app_vac.models import Company


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    password2 = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        return password1


class MyCompanyForm(forms.Form):
    name = forms.CharField(label='Название компании', max_length=100)
    count_people = forms.CharField(label='Количество человек в компании', max_length=32)
    logo = forms.ImageField(label='Логотип')
    location = forms.CharField(label='География', max_length=100)
    info = forms.CharField(widget=forms.Textarea)

    '''class Meta:
        model = Company
        fields = '__all__'''


class ApplicationsForm(forms.Form):
    name = forms.CharField(label='Вас зовут', max_length=100)
    phone = forms.CharField(label='ваш телефон', max_length=100)
    letter = forms.CharField(widget=forms.Textarea)