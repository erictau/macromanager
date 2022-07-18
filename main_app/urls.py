from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('index/', views.index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('organizations/', views.organizations_index, name='organizations_index'), 
    path('organizations/create', views.organizations_create, name='organizations_create'),
    path('departments/', views.DepartmentList.as_view(), name='department_index'), 
    path('departments/<int:pk>', views.DepartmentDetail.as_view(), name='department_detail'),

]