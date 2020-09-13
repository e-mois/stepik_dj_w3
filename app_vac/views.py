from django.http import Http404, HttpResponseServerError
from django.shortcuts import render
from django.views import View

from app_vac.models import Speciality, Vacancy, Company


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
        vac_dict = {}
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

        for vacancy in vacancies:
            vac_dict[vacancy.id] = {}
            vac_dict[vacancy.id]["title"] = vacancy.title
            vac_dict[vacancy.id]["skills"] = vacancy.skills
            vac_dict[vacancy.id]["description"] = vacancy.description
            vac_dict[vacancy.id]["salary_min"] = vacancy.salary_min
            vac_dict[vacancy.id]["salary_max"] = vacancy.salary_max
            vac_dict[vacancy.id]["date"] = vacancy.published_at
            vac_dict[vacancy.id]["company"] = vacancy.company.name
            vac_dict[vacancy.id]["company_id"] = vacancy.company.id
            vac_dict[vacancy.id]['company_pic'] = vacancy.company.logo
            vac_dict[vacancy.id]["spec"] = vacancy.speciality.name

        context["vacancies"] = vac_dict

        return render(request, 'vacancies.html', context=context)


class CompanyView(View):
    def get(self, request, company_id):
        if company_id is None:
            raise Http404
        company = Company.objects.get(id=company_id)
        vacancies = Vacancy.objects.filter(company=company_id)
        vac_dict = {}
        for vacancy in vacancies:
            vac_dict[vacancy.id] = {}
            vac_dict[vacancy.id]["title"] = vacancy.title
            vac_dict[vacancy.id]["skills"] = vacancy.skills
            vac_dict[vacancy.id]["description"] = vacancy.description
            vac_dict[vacancy.id]["salary_min"] = vacancy.salary_min
            vac_dict[vacancy.id]["salary_max"] = vacancy.salary_max
            vac_dict[vacancy.id]["date"] = vacancy.published_at
            vac_dict[vacancy.id]["company"] = vacancy.company.name
            vac_dict[vacancy.id]["company_id"] = vacancy.company.id
            vac_dict[vacancy.id]['company_pic'] = vacancy.company.logo
            vac_dict[vacancy.id]["spec"] = vacancy.speciality.name

        context = {
            'company': company,
            'vacancies': vac_dict
        }
        return render(request, 'company.html', context=context)


class VacancySingleView(View):
    def get(self, request, vacancy_id):
        if vacancy_id is None:
            raise Http404
        vacancy = Vacancy.objects.get(id=vacancy_id)

        context = {
            'vacancy': vacancy,
        }
        return render(request, 'vacancy.html', context=context)
