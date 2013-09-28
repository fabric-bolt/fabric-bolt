from django.core.urlresolvers import reverse
from django.db import models

from core.mixins.models import TrackingFields

from model_managers import ActiveManager


class ProjectType(TrackingFields):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s' % self.name


class Project(TrackingFields):
    """Model for a project (pretty obvious)

    Keeps track of the stages and general configurations for deployments"""

    name = models.CharField(max_length=255)

    type = models.ForeignKey(ProjectType, blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    # Misc information for a project
    number_of_deployments = models.IntegerField(default=0)

    # Managers
    objects = models.Manager()
    active_records = ActiveManager()
    # End Managers

    def project_configurations(self):
        return Configuration.objects.filter(project_id=self.pk, stage__isnull=True)

    def __unicode__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('projects_project_view', args=(self.pk,))


class Stage(TrackingFields):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=255)

    # Managers
    objects = models.Manager()
    active_records = ActiveManager()
    # End Managers

    def __unicode__(self):
        return self.name

    def stage_configurations(self):
        return Configuration.objects.filter(stage=self)

    def get_absolute_url(self):
        """Go back to the project page"""
        return self.project.get_absolute_url()

    def get_configurations(self):
        """Generates a dictionary that's made up of the configurations on the project

        Any configurations on a project that are duplicated on a stage, the stage configuration will take precedence.
        """
        pass


class Configuration(TrackingFields):
    project = models.ForeignKey(Project)
    stage = models.ForeignKey(Stage, null=True, blank=True)

    key = models.CharField(max_length=255)
    value = models.CharField(max_length=500, null=True, blank=True)

    # Managers
    objects = models.Manager()
    active_records = ActiveManager()
    # End Managers

    def __unicode__(self):
        return '{}: {}'.format(self.key, self.value)

    def get_absolute_url(self):
        """Go back to the project page"""

        if self.stage:
            url = reverse('projects_stage_view', args=(self.project.pk, self.stage.pk))
        else:
            url = self.project.get_absolute_url()

        return url


class Deployment(TrackingFields):
    PENDING = 'pending'
    FAILED = 'failed'
    SUCCESS = 'success'

    STATUS = [(PENDING, 'Pending'), (FAILED, 'Failed'), (SUCCESS, 'Success')]

    stage = models.ForeignKey(Stage)
    comments = models.TextField()
    status = models.CharField(choices=STATUS, max_length=10)
    output = models.TextField(null=True, blank=True)
    task = models.ForeignKey('projects.Task')

    # Managers
    objects = models.Manager()
    active_records = ActiveManager()
    # End Managers

    def __unicode__(self):
        return "Deployment at {} for stage {} on project {}".format(self.date_created, self.stage.name, self.stage.project.name)


class Task(models.Model):
    name = models.CharField(max_length=255)
    times_used = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.times_used)
