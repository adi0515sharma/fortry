from django.contrib import admin

from .models import WorkingDays, LeaveApplication

admin.site.register(WorkingDays)
admin.site.register(LeaveApplication)