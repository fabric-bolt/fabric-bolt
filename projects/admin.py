from django.contrib import admin

import models

admin.site.register(models.Project)
admin.site.register(models.ProjectType)
admin.site.register(models.Configuration)
admin.site.register(models.Stage)