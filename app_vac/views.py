import datetime

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from app_vac.forms import ApplicationsForm, MyCompanyForm, MyUserCreationForm, VacancyForm
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
        user = request.user
        form = self.form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            letter = form.cleaned_data['letter']
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
                                          'location': my_company.location, 'info': my_company.description},
                                 auto_id=False)
            context = {'form': form}
            return render(request, 'company-edit.html', context=context)
        else:
            return render(request, 'company-create.html')

    def post(self, request):
        form = MyCompanyForm(request.POST, request.FILES)
        my_company = Company.objects.filter(owner=request.user)[0]

        if form.is_valid():
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = filename

            my_company.name = form.cleaned_data['name']
            my_company.employee_count = form.cleaned_data['count_people']
            my_company.logo = uploaded_file_url
            my_company.location = form.cleaned_data['location']
            my_company.description = form.cleaned_data['info']

            my_company.save()
            messages.success(request, 'Company updated successfully')
            return redirect('/mycompany/')
        else:
            return redirect('/mycompany/')


class MyCompanyCreateView(View):
    def get(self, request):
        form = MyCompanyForm()
        context = {'form': form}
        return render(request, 'company-edit.html', context=context)

    def post(self, request):
        user = request.user
        form = MyCompanyForm(request.POST, request.FILES)

        if form.is_valid():
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = filename

            name = form.cleaned_data['name']
            count_people = form.cleaned_data['count_people']
            logo = uploaded_file_url
            location = form.cleaned_data['location']
            info = form.cleaned_data['info']
            new_company = Company(name=name, employee_count=count_people,
                                  logo=logo, location=location, description=info, owner=user)
            new_company.save()
            return redirect('/mycompany/')
        else:
            return render(request, 'company-edit.html', context={'form': form})


class MyCompanyVacanciesListView(View):
    def get(self, request):
        my_company = Company.objects.filter(owner=request.user.id)[0]
        vacancies_list = Vacancy.objects.filter(company=my_company)
        context = {
            'vac_list': vacancies_list,
        }
        return render(request, 'vacancy-list.html', context=context)


class MyCompanyVacancyCreate(View):
    def get(self, request):
        form = VacancyForm()
        speciality_list = [x.name for x in Speciality.objects.all()]
        context = {'form': form, 'specs': speciality_list}
        return render(request, 'vacancy-edit.html', context=context)

    def post(self, request):
        user = request.user
        my_company = Company.objects.filter(owner=user)[0]
        form = VacancyForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            company = my_company
            skills = form.cleaned_data['skills'],
            speciality = form.cleaned_data['speciality']
            description = form.cleaned_data['description'],
            salary_min = form.cleaned_data['salary_min'],
            salary_max = form.cleaned_data['salary_max'],
            published_at = datetime.datetime.today().strftime("%Y-%m-%d")
            new_vac = Vacancy(title=title,
                              speciality=speciality,
                              company=company,
                              skills=skills,
                              description=description,
                              salary_min=salary_min,
                              salary_max=salary_max,
                              published_at=published_at)
            new_vac.save()

            return redirect('/mycompany/vacancies/')


class MyCompanyVacancyEdit(View):
    def get(self, request, vacancy_id):
        my_vacancy = Vacancy.objects.get(id=vacancy_id)
        vacancy_applications = Applications.objects.filter(vacancy_id=vacancy_id)
        if my_vacancy:
            form = VacancyForm(initial={'title': my_vacancy.title,
                                        'speciality': my_vacancy.speciality.name,
                                        'company': my_vacancy.company, 'skills': my_vacancy.skills,
                                        'description': my_vacancy.description, 'salary_min': my_vacancy.salary_min,
                                        'salary_max': my_vacancy.salary_max, 'published_at': my_vacancy.published_at},
                               auto_id=False)
            context = {'form': form, 'vac_app': vacancy_applications, 'vac': my_vacancy}
            return render(request, 'vacancy-edit.html', context=context)
        else:
            return render(request, 'vacancy-edit.html')

    def post(self, request, vacancy_id):
        my_vacancy = Vacancy.objects.get(id=vacancy_id)
        form = VacancyForm(request.POST)
        if form.is_valid():
            my_vacancy.title = form.cleaned_data['title']
            my_vacancy.skills = form.cleaned_data['skills']
            my_vacancy.speciality = Speciality.objects.get(id=form.cleaned_data['speciality'])
            my_vacancy.description = form.cleaned_data['description']
            my_vacancy.salary_min = form.cleaned_data['salary_min']
            my_vacancy.salary_max = form.cleaned_data['salary_max']
            my_vacancy.published_at = datetime.datetime.today().strftime("%Y-%m-%d")
            my_vacancy.save()
            messages.success(request, 'Vacancy updated successfully')
            return redirect(f'/mycompany/vacancies/{vacancy_id}/')
        else:
            return redirect('/mycompany/vacancies/')
