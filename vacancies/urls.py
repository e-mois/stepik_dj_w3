"""vacancies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from app_vac.views import CompanyView, MainView, MyLoginView, MySignupView, VacanciesView, VacancySingleView, \
    MyCompanyView, MyCompanyCreateView, MyCompanyVacanciesListView, ApplicationSent, MyCompanyVacancyCreate, \
    MyCompanyVacancyEdit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='index'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:vac_category>/', VacanciesView.as_view()),
    path('companies/<int:company_id>/', CompanyView.as_view()),
    path('vacancies/<int:vacancy_id>/', VacancySingleView.as_view()),
    path('vacancies/<int:vacancy_id>/send/', ApplicationSent.as_view()),
    path('login/', MyLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', MySignupView.as_view()),
    path('mycompany/', MyCompanyView.as_view(), name='mycompany'),
    path('mycompany/create/', MyCompanyCreateView.as_view()),
    path('mycompany/vacancies/', MyCompanyVacanciesListView.as_view(), name='vac_list'),
    path('mycompany/vacancies/create/', MyCompanyVacancyCreate.as_view(), name='company-vac-create'),
    path('mycompany/vacancies/<int:vacancy_id>/', MyCompanyVacancyEdit.as_view(), name='company-vac-edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
