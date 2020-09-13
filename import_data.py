from data import jobs, companies, specialties
from app_vac.models import Company, Speciality, Vacancy


def import_specialties(specialties):
    for spec in specialties:
        new_spec = Speciality(code=spec["code"], picture=f'specialties/specty_{spec["code"]}.png')
        new_spec.save()


def import_company(companies):
    for company in companies:
        new_company = Company(name=company["title"], employee_count=0)
        new_company.save()


def import_vacancy(vacancies):
    for vacancy in vacancies:
        spec = Speciality.objects.filter(code=vacancy['cat'])[0]
        company = Company.objects.filter(name=vacancy['company'])[0]
        new_vacancy = Vacancy(title=vacancy["title"], salary_min=vacancy["salary_from"],
                              salary_max=vacancy["salary_to"], published_at=vacancy['posted'],
                              description=vacancy["desc"], speciality=spec, company=company)
        new_vacancy.save()


if __name__ == "__main__":
    import_specialties(specialties)
    import_company(companies)
    import_vacancy(jobs)
