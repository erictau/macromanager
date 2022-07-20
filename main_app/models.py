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
EMPROLES = (
    ('OWN', 'Owner'), 
    ('MGR', 'Manager'), 
    ('MBR', 'Staff Member')
)

# Create your models here,
class Organization(models.Model):
    name = models.CharField(max_length=30, unique=True)

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
    status = models.CharField(
        max_length=3, 
        choices=TASKSTATUS, 
        default=TASKSTATUS[0][0]
        )
    urgency = models.CharField(
        max_length=5,
        choices=TASKURGENCY, 
        default=TASKURGENCY[0][0]
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-due']

class Employee(models.Model):
    # role = models.CharField(
    #     max_lenght=3, 
    #     choices=EMPROLES,
    #     default=EMPROLES[0][0])
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dept = models.ManyToManyField(Department)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task)

    # def __str__(self):
    #     return self.user_id.first_name

