"""Some generic model mixins"""

from django.db import models


class TrackingFields(models.Model):
    """Generic  model for some generic fields related to when a record was created, updated and deleted

    In some cases the date_delete field is not useful since the actual record won't be there. However,
    we're using it for archiving an object and have an active_records model manager."""
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    date_deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True