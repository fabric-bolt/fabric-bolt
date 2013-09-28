"""Some generic model mixins"""

from django.db import models


class TrackingFields(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    date_deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True