from django.contrib import admin
from .models import devices,order,Project, supplement
# Register your models here.
admin.site.register(devices)
admin.site.register(order)
admin.site.register(Project)
admin.site.register(supplement)