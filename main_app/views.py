from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import OrgForm, UserForm, DeptForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Department, Organization


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    pass

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('organizations_new')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


### Organization 

@login_required
def organizations_new(request):
    orgs = Organization.objects.all()
    org_form = OrgForm()
    context = { 'orgs': orgs, 'org_form': org_form }
    return render(request, 'organizations/organization_form.html', context)

@login_required
def organizations_create(request):
    form = OrgForm(request.POST)
    if form.is_valid():
        # This is where we would associate an org to an employee id.
        form.save()
    return redirect('departments_new')


### Departments

@login_required
def departments_new(request):
    dept = Department.objects.all()
    dept_form = DeptForm()
    context = { 'dept': dept, 'dept_form': dept_form}
    return render(request, 'departments/department_form.html', context)

@login_required
def tasks_create(request, department_id):
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.department_id = department_id
        task.save()
    return redirect('department_detail', department_id = department_id)

@login_required
def departments_create(request):
    form = DeptForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('')
    

def task_update(request):
    pass