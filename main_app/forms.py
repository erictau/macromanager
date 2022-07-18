from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from main_app.models import Organization, Department

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

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name']