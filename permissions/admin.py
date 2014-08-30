from django.contrib import admin

from permissions.models import *


admin.site.register(GlobalPermission)
admin.site.register(ProjectPermission)
