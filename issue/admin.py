from django.contrib import admin
from issue.models import *

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Event)
admin.site.register(Label)
admin.site.register(Milestone)
admin.site.register(Settings)
admin.site.register(Team)
admin.site.register(GlobalPermission)
admin.site.register(ProjectPermission)
