from django.contrib import admin

from tracker.models import *


admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Label)
admin.site.register(Milestone)
admin.site.register(Event)
