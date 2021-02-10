from django.contrib import admin

from .models import Event, Approval, Feedback
admin.site.register(Event)
admin.site.register(Feedback)
admin.site.register(Approval)
