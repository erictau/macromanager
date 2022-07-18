from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('index/', views.index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('organizations/create/', views.OrganizationCreate.as_view(), name='organization_create'), # Eric: May need to change this to a custom view function.
    path('departments/', views.DepartmentList.as_view(), name='department_index'), 
    path('departments/<int:pk>', views.DepartmentDetail.as_view(), name='department_detail'),

]