from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import OrgForm, UserForm, DeptForm, TaskForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView


from .models import Department, Organization, Task, Employee


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
    org = Organization.objects.get(name=request.POST['name'])
    Employee.objects.create(user_id=request.user.id, org_id=org.id)
    return redirect('departments_index')

@login_required
def assoc_org_employee(request):
    Employee.objects.create(user_id=request.user.id, org_id=request.POST['org_id'])
    return redirect('home')


### Departments

@login_required
def departments_index(request):
    depts = Department.objects.filter(org_id = request.user.employee.org_id)
    dept_form = DeptForm()
    context = { 'depts': depts, 'dept_form': dept_form}
    return render(request, 'departments/department_form.html', context)

@login_required
def departments_create(request):
    form = DeptForm(request.POST)
    if form.is_valid():
        department = form.save(commit=False)
        department.org_id = request.user.employee.org.id
        form.save()
    return redirect('departments_index')

@login_required
def departments_detail(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if department.org_id != request.user.employee.org_id:
        return redirect('departments_index')
    task_form = TaskForm()
    tasks = department.task_set.all()
    print(tasks)
    return render(request, 'departments/department_detail.html', {'department':department, 'tasks': tasks, 'task_form': task_form })

class DepartmentDelete(LoginRequiredMixin, DeleteView):
	model = Department
	success_url = "/"

### Tasks

@login_required
def tasks_create(request, department_id):
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.department_id = department_id
        task.save()
    return redirect('departments_detail', department_id = department_id)

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    def get_success_url(self, **kwargs):
        return reverse('departments_detail', args=[self.kwargs['department_id']])

### Employees

def employees_detail(request, employee_id):
    tasks = employee.task_set.all()
    return render(
        request, 
        'employees/detail.html', 
        {'tasks': tasks, })
