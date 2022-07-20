from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from main_app.models import Organization, Department, Task

class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'password1' ,'password2' )

class OrgForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name']

class DeptForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class TaskForm(forms.Form):
        # model = Task
        name = forms.CharField()
        date = forms.DateField(widget = forms.SelectDateWidget)
        description = forms.CharField(widget = forms.Textarea)
        status = forms.CharField()
        urgency = forms.CharField()
        