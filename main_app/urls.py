from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('index/', views.index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('organizations/new', views.organizations_new, name='organizations_new'), 
    path('organizations/create', views.organizations_create, name='organizations_create'),
    path('departments/index', views.departments_index, name='departments_index'), 
    path('departments/create', views.departments_create, name='departments_create'),
    path('departments/<int:department_id>/', views.departments_detail, name='departments_detail'),
    path('departments/<int:department_id>/tasks_create', views.tasks_create, name='tasks_create'),
    path('tasks/<int:pk>', views.TaskDetail.as_view(), name='tasks_detail'),
    path('departments/<int:department_id>/tasks/<int:pk>/delete', views.TaskDelete.as_view(), name='tasks_delete'),

]