from django.contrib import admin

from .models import Hardware, Software, Vendor

admin.site.register(Hardware)
admin.site.register(Software)
admin.site.register(Vendor)