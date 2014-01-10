from django.contrib import admin
from fabric_bolt.hosts import models

admin.site.register(models.Host)