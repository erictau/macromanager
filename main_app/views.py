from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserForm
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
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


### Organization 
# Eric: Since we're creating an organization in the signup process, we may need to change this from a class based view to a custom view function. This is so we can add code that associates the logged in user with the organization that was just created. 
class OrganizationCreate(LoginRequiredMixin, CreateView):
    model = Organization
    fields = '__all__'

# Eric: Department Index will contain a list of all departments in an organization, and also a form for creating new Departments. Therefore, the CBV DepartmentCreate is not required. Instead, we will need to create a custom view function.
class DepartmentList(LoginRequiredMixin, ListView):
    model = Department

class DepartmentDetail(LoginRequiredMixin, DetailView):
    model = Department
    

