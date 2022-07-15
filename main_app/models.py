from django.db import models
from datetime import date
from django.contrib.auth.models import User


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

# Create your models here,
class Organization(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=30)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=50)
    due = models.DateField('Due Date')
    description = models.TextField(max_length=300)
    status = models.CharField(max_length=100)
    urgency = models.CharField(
        max_length=5,
        choices=TASKURGENCY, 
        default=TASKURGENCY[0][0]
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dep = models.ForeignKey(Department)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

