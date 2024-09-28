from django.contrib import admin
from resources.models import ResourceDetail, ProjectDetail, TaskInfo

# Register your models here.

admin.site.register(ResourceDetail)
admin.site.register(ProjectDetail)
admin.site.register(TaskInfo)
