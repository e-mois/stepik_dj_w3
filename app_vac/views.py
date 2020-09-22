from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import Http404, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from app_vac.forms import ApplicationsForm, MyCompanyForm, MyUserCreationForm
from app_vac.models import Speciality, Vacancy, Company, Applications


def custom_handler500(request):
    return HttpResponseServerError('Ой, что-то сервер потерялся! ')


class MainView(View):
    def get(self, request):
        specs = Speciality.objects.all()
        companies = Company.objects.all()

        specs_dict = {}
        for spec in specs:
            vac_count = len(Vacancy.objects.filter(speciality=spec.id))
            specs_dict[spec.code] = {}
            specs_dict[spec.code]["name"] = spec.name
            specs_dict[spec.code]['count'] = vac_count
            specs_dict[spec.code]['pic'] = spec.picture

        companies_dict = {}
        for company in companies:
            vac_count_company = len(Vacancy.objects.filter(company=company.id))
            companies_dict[company.name] = {}
            companies_dict[company.name]["id"] = company.id
            companies_dict[company.name]['logo'] = company.logo
            companies_dict[company.name]['count'] = vac_count_company

        context = {
            "specs": specs_dict,
            "companies": companies_dict
        }

        return render(request, 'index.html', context=context)


class VacanciesView(View):
    def get(self, request, vac_category=""):
        context = {}
        if vac_category:
            spec = Speciality.objects.filter(code=vac_category)[0]
            vacancies = Vacancy.objects.filter(speciality=spec.id)
            if vacancies is None:
                raise Http404
            else:
                context["all_vac"] = False
                context["title_vac"] = spec.name
        else:
            vacancies = Vacancy.objects.all()
            context["all_vac"] = True

        context["vacancies"] = vacancies

        return render(request, 'vacancies.html', context=context)


class CompanyView(View):
    def get(self, request, company_id):
        if company_id is None:
            raise Http404
        company = Company.objects.get(id=company_id)
        vacancies = Vacancy.objects.filter(company=company_id)

        context = {
            'company': company,
            'vacancies': vacancies
        }
        return render(request, 'company.html', context=context)


class VacancySingleView(View):
    form = ApplicationsForm

    def get(self, request, vacancy_id):
        if vacancy_id is None:
            raise Http404
        vacancy = Vacancy.objects.get(id=vacancy_id)
        form = self.form
        context = {
            'vacancy': vacancy,
            'form': form
        }
        return render(request, 'vacancy.html', context=context)

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        user = User.objects.filter(username=request.user)[0]
        form = self.form(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            letter = request.POST.get('letter')
            new_app = Applications(written_username=name, written_phone=phone,
                                   written_cover_letter=letter, vacancy=vacancy, user=user)
            new_app.save()
        return redirect(f'{vacancy_id}/send')


class MySignupView(CreateView):
    form_class = MyUserCreationForm
    success_url = 'login'
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        return super(MySignupView, self).form_valid(form)


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class ApplicationSent(View):
    def get(self, request, vacancy_id):
        context = {
            'id': vacancy_id
        }
        return render(request, 'sent.html', context=context)


class MyCompanyView(View):
    def get(self, request):
        company = Company.objects.filter(owner=request.user.id)
        if company:
            my_company = company[0]
            form = MyCompanyForm(initial={'name': my_company.name, 'count_people': my_company.employee_count,
                                          'logo': my_company.logo.url, 'location': my_company.location,
                                          'info': my_company.description},
                                 auto_id=False)
            context = {'form': form}
            return render(request, 'company-edit.html', context=context)
        else:
            return render(request, 'company-create.html')

    def post(self, request):
        form = MyCompanyForm(request.POST)
        my_company = Company.objects.filter(owner=request.user)[0]
        if form.is_valid():
            my_company.name = request.POST.get('name')
            my_company.employee_count = request.POST.get('count_people')
            my_company.logo = request.POST.get('logo')
            my_company.location = request.POST.get('location')
            my_company.description = request.POST.get('info')

            my_company.save()
            return redirect('mycompany')


class MyCompanyCreateView(View):
    def get(self, request):
        form = MyCompanyForm()
        context = {'form': form}
        return render(request, 'company-edit.html', context=context)

    def post(self, request):
        user = User.objects.filter(username=request.user)[0]
        form = MyCompanyForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            count_people = request.POST.get('count_people')
            logo = request.POST.get('logo')
            location = request.POST.get('location')
            info = request.POST.get('info')
            new_company = Company(name=name, employee_count=count_people,
                                  logo=logo, location=location, description=info, owner=user)
            new_company.save()
            return redirect('mycompany')
        else:
            return render(request, 'company-edit.html', context={'form': form})


class MyCompanyVacanciesListView(View):
    def get(self, request):
        return render(request, 'vacancy-list.html')
