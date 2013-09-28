from django.db import models


class ProjectConfigurationsManager(models.Manager):
    def get_query_set(self):
        return super(ProjectConfigurationsManager, self).get_query_set().filter(stage=None)


class StageConfigurationsManager(models.Manager):
    def get_query_set(self):
        return super(ProjectConfigurationsManager, self).get_query_set().filter(stage=None)