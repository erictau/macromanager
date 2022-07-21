from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from main_app.models import Organization, Department, Task, Employee

TASKURGENCY = (
    ('LOW', 'Low Priority'), 
    ('MID', 'Medium Priority'), 
    ('HIGH', 'High Priority'), 
    ('EMERG', 'EMERGENCY PRIORITY!')
)
TASKSTATUS = (
    ('IP', 'In Progress'), 
    ('AS', 'Assigned'), 
    ('UAS', 'Unassigned'), 
    ('COM', 'Complete'), 
)

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
        name = forms.CharField(initial = 'Task')
        due = forms.DateField(widget = forms.SelectDateWidget)
        description = forms.CharField(widget = forms.Textarea)
        status = forms.MultipleChoiceField(choices = TASKSTATUS)
        urgency = forms.MultipleChoiceField(choices = TASKURGENCY)
