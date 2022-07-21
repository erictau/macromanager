from telnetlib import STATUS
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
    if request.user.id:
        return redirect('home')
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
    if hasattr(request.user, 'employee') and hasattr(request.user.employee, 'org_id'):
        return redirect('home')
    orgs = Organization.objects.all()
    org_form = OrgForm()
    context = { 'orgs': orgs, 'org_form': org_form }
    return render(request, 'organizations/organization_form.html', context)

@login_required
def organizations_create(request):
    if hasattr(request.user, 'employee') and hasattr(request.user.employee, 'org_id'):
        return redirect('home')
    form = OrgForm(request.POST)
    if form.is_valid():
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
    # employees = list(Employee.objects.filter(dept = department_id))
    employees = department.employee_set.all()
    return render(request, 'departments/department_detail.html', {'department':department, 'tasks': tasks, 'task_form': task_form, 'employees': employees })

class DepartmentUpdate(LoginRequiredMixin, UpdateView):
    model = Department
    fields = ['name']
    template_name = 'departments/department_update.html'

class DepartmentDelete(LoginRequiredMixin, DeleteView):
	model = Department
	success_url = "/"

### Tasks

@login_required
def tasks_create(request, department_id):
    dat_form = TaskForm(request.POST)

    if dat_form.is_valid():

        clean_form = dat_form.cleaned_data
        print(clean_form)

        all_together_now = Task(
            name = clean_form['name'],
            due = clean_form['due'],
            description = clean_form['name'],
            status = clean_form['status'][0],
            urgency = clean_form['urgency'][0],
            department_id = department_id 
        )
        all_together_now.save()

    # new_task = Task.objects.create(
    #     name = request.POST.get('name'), due = request.POST.get('due'), description = request.POST.get('description'),
    #     status = request.POST.get('status'), urgency = request.POST.get('urgency'), department_id = department_id
    #  )

    # Eric: Icebox - Figure out how to validate the request.POST data before saving to DB.
    # new_task_dict = {}
    # for prop in request.POST:
    #     new_task_dict[prop] = request.POST[prop]
    # # new_task_dict['department_id'] = department_id
    # print(new_task_dict)
    # request.POST.department_id = department_id
    # task_form = TaskForm(new_task_dict)
    # print(task_form.instance)
    # if task_form.is_valid():
    #     task_form.save(commit=False)
    #     task_form.department_id = department_id
    #     task_form.save()
    return redirect('departments_detail', department_id = department_id)

# class TaskDetail(LoginRequiredMixin, DetailView):
#     model = Task
#     template_name = 'tasks/detail.html'

@login_required
def tasks_detail(request, task_id):
    task = Task.objects.get(id = task_id)
    employee = Employee.objects.get(id = request.user.employee.id)
    avlemp = Employee.objects.filter(org_id = employee.org.id).exclude(id__in=task.employee_set.all())
    asgnemp = Employee.objects.filter(id__in=task.employee_set.all())
    print(asgnemp)
    return render(request, 'tasks/detail.html', {'employee':employee, 'task':task, 'avlemp':avlemp, 'asgnemp':asgnemp})

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/form.html'
    form_class = TaskForm
    # Creating the custom task form may make it slightly more difficult to use CBV's to update the task. 
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    def get_success_url(self, **kwargs):
        return reverse('departments_detail', args=[self.kwargs['department_id']])

@login_required
def assoc_task_employee(request, task_id):
    task = Task.objects.get(id = task_id)
    employee = Employee.objects.get(id = request.POST['employee'])
    employee.task.add(task_id)
    return redirect('tasks_detail', task_id)

def remove_task_employee(request, task_id):
    task = Task.objects.get(id = task_id)
    employee = Employee.objects.get(id = request.POST['employee'])
    employee.task.remove(task_id)
    return redirect('tasks_detail', task_id)


### Employees

@login_required
def employees_detail(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    tasks = employee.task.all()
    departments = employee.dept.all()
    excludedept = employee.dept.all().values_list('id')
    avldepts = Department.objects.filter(org_id = employee.org_id).exclude(id__in=excludedept)
    return render(
        request, 
        'employees/employee_detail.html', 
        {'tasks': tasks, 'employee': employee, 'departments': departments, 'avldepts': avldepts})

@login_required
def employees_index(request):
    employees = Employee.objects.filter(org_id = request.user.employee.org_id)
    return render(request, 'employees/employee_index.html',{'employees': employees})

# @login_required
def assoc_dept_employee(request, employee_id): 
    employee = Employee.objects.get(id = employee_id)
    employee.dept.add(request.POST['dept'])
    return redirect('employees_detail', employee_id)

