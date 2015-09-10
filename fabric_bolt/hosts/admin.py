from django.contrib import admin

from fabric_bolt.hosts import models

@admin.register(models.SSHConfig)
class SSHConfigAdmin(admin.ModelAdmin):
    exclude = ['private_key_file']
    readonly_fields = ['name', 'public_key', 'remote_user']

    def has_add_permission(self, request):
        return False

admin.site.register(models.Host)
