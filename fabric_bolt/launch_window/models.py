
from django.db import models


class LaunchWindow(models.Model):
    """Defines a period of time that deployments can be made in"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    cron_format = models.CharField(max_length=255, blank=True, null=True)  # '* 09-17 * * 1-4': 9AM-5PM Mon-Thurs.

    def __unicode__(self):
        return self.name