from django.contrib import admin
from fabric_bolt.projects import models


class ConfigurationModelAdmin(admin.ModelAdmin):
    list_display = ['project', 'stage', 'key', 'value']


class DeploymentModelAdmin(admin.ModelAdmin):
    list_display = ['stage', 'status', 'date_created', 'task']


admin.site.register(models.Project)
admin.site.register(models.ProjectType)
admin.site.register(models.Configuration, ConfigurationModelAdmin)
admin.site.register(models.Stage)
admin.site.register(models.Deployment, DeploymentModelAdmin)
admin.site.register(models.Task)