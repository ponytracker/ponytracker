from django.contrib import admin
from issue.models import *

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Event)
admin.site.register(Label)
admin.site.register(Milestone)
