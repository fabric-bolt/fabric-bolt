from django.db import models

from fabric_bolt.core.mixins.models import TrackingFields

from fabric_bolt.projects.models import Project

from .managers import HookManager


class Hook(TrackingFields):

    # If this project is null then it's a global hook
    project = models.ForeignKey(Project, blank=True, null=True)

    url = models.URLField()

    # Custom manager to allow us to look up the proper hooks
    objects = HookManager()

    def __unicode__(self):
        return u'{}'.format(self.url)
