from django.db import models


class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(date_deleted__isnull=True)


class ActiveDeploymentManager(models.Manager):
    def get_query_set(self):
        return super(ActiveDeploymentManager, self).get_query_set()\
            .filter(date_deleted__isnull=True,
                    stage__date_deleted__isnull=True,
                    stage__project__date_deleted__isnull=True)