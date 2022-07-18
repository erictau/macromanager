from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('index/', views.index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('organizations/new', views.organizations_new, name='organizations_new'), 
    path('organizations/create', views.organizations_create, name='organizations_create'),
    path('departments/new', views.departments_new, name='departments_new'), 
]