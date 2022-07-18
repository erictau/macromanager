from django.contrib import admin
from .models import Organization, Department, Task, Employee

# Register your models here.
admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Task)
admin.site.register(Employee)
