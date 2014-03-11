from django.core.urlresolvers import reverse
from django.db.models import Count, Sum
from django.db import models
from django.contrib.auth import get_user_model

from fabric_bolt.core.mixins.models import TrackingFields

from fabric_bolt.projects.model_managers import ActiveManager


class ProjectType(TrackingFields):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name



class Project(TrackingFields):
    """Model for a project (pretty obvious)

    Keeps track of the stages and general configurations for deployments"""

    name = models.CharField(max_length=255)

    type = models.ForeignKey(ProjectType, blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    # Managers
    objects = models.Manager()
    active_records = ActiveManager()
    # End Managers

    def project_configurations(self):
        return Configuration.objects.filter(project_id=self.pk, stage__isnull=True)

    def __unicode__(self):
        return self.name

    def get_stages(self):
        """Utility function that returns the stages on a specific project"""

        return Stage.active_records.filter(project=self)

    def get_absolute_url(self):
        """Let's see the project detail page now."""

        return reverse('projects_project_view', args=(self.pk,))

    def get_deployment_count(self):
        """Utility function to get the number of deployments a given project has"""

        ret = self.stage_set.annotate(num_deployments=Count('deployment')).aggregate(total_deployments=Sum('num_deployments'))
        return ret['total_deployments']


class Stage(TrackingFields):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=255)
    hosts = models.ManyToManyField('hosts.Host')

    # Managers
    objects = models.Manager()
    active_records = ActiveManager()
    # End Managers

    def __unicode__(self):
        return self.name

    def stage_configurations(self):
        """Helper function that returns the stage specific configurations"""

        return Configuration.objects.filter(stage=self)

    def get_absolute_url(self):
        """Stages are show on a project page so that's where we're sending you to see them"""

        return self.project.get_absolute_url()

    def get_queryset_configurations(self, **kwargs):
        """
        Really we just want to do a simple SQL statement like this (but oh the ORM):

        SELECT Distinct(Coalesce(stage.key, project.key)) AS key,
        (CASE WHEN stage.key IS NOT null THEN stage.data_type ELSE project.data_type END) AS data_type,
        (CASE WHEN stage.key IS NOT null THEN stage.value ELSE project.value END) AS value,
        (CASE WHEN stage.key IS NOT null THEN stage.value_number ELSE project.value_number END) AS value_number,
        (CASE WHEN stage.key IS NOT null THEN stage.value_boolean ELSE project.value_boolean END) AS value_boolean,
        (CASE WHEN stage.key IS NOT null THEN stage.prompt_me_for_input ELSE project.prompt_me_for_input END) AS prompt_me_for_input,
        (CASE WHEN stage.key IS NOT null THEN stage.sensitive_value ELSE project.sensitive_value END) AS sensitive_value
        FROM projects_configuration AS project
        LEFT JOIN projects_configuration AS stage ON stage.project_id = project.project_id
            AND project.key = stage.key AND stage.stage_id = STAGE_ID_HERE
        WHERE project.project_id = PROJECT_ID_HERE AND (project.stage_id is null OR project.stage_id = STAGE_ID_HERE)
        """
        queryset_list = []
        current_configs = []

        # Create stage specific configurations dictionary
        for stage in self.stage_configurations().filter(**kwargs):
            queryset_list.append(stage)
            current_configs.append(stage.key)

        for project in self.project.project_configurations().filter(**kwargs):
            if not project.key in current_configs:
                queryset_list.append(project)
                current_configs.append(project.key)

        return queryset_list

    def get_configurations(self):
        """
        Generates a dictionary that's made up of the configurations on the project.
        Any configurations on a project that are duplicated on a stage, the stage configuration will take precedence.
        """

        project_configurations_dictionary = {}
        project_configurations = self.project.project_configurations()

        # Create project specific configurations dictionary
        for config in project_configurations:
            project_configurations_dictionary[config.key] = config.get_value()

        stage_configurations_dictionary = {}
        stage_configurations = self.stage_configurations()

        # Create stage specific configurations dictionary
        for s in stage_configurations:
            stage_configurations_dictionary[s.key] = s.get_value()

        # override project specific configuration with the ones in the stage if they are there
        project_configurations_dictionary.update(stage_configurations_dictionary)

        # Return the updated configurations
        return project_configurations_dictionary


class Configuration(TrackingFields):
    """Configurations can be on a project or a specific stage.

    If a configuration value is found on both a project and a stage then the stage's configuration value will be the
    one used.

    These are key:value pairs that are pumped into the fab script via the command line. Inside your fab script you'll
    have access to env.key (env.server_ip, env.port_number, etc).
    """

    BOOLEAN_TYPE = 'boolean'
    NUMBER_TYPE = 'number'
    STRING_TYPE = 'string'

    DATA_TYPES = ((BOOLEAN_TYPE, 'Boolean'), (NUMBER_TYPE, 'Number'), (STRING_TYPE, 'String'))

    project = models.ForeignKey(Project)
    stage = models.ForeignKey(Stage, null=True, blank=True)

    key = models.CharField(max_length=255)
    value = models.CharField(max_length=500, null=True, blank=True)
    value_number = models.FloatField(verbose_name='Value', null=True, blank=True, default=0)
    value_boolean = models.BooleanField(verbose_name='Value', default=False)
    data_type = models.CharField(choices=DATA_TYPES, null=True, blank=True, max_length=10, default=STRING_TYPE)

    prompt_me_for_input = models.BooleanField(default=False, help_text='When deploying you will be prompted for this value.')
    sensitive_value = models.BooleanField(default=False, help_text='Password or other value that should not be stored in the logs.')

    # Managers
    objects = models.Manager()
    active_records = ActiveManager()
    # End Managers

    def __unicode__(self):
        return u'{}: {}'.format(self.key, self.value)

    def get_absolute_url(self):
        """Determine where I am coming from and where I am going"""

        # Determine if this configuration is on a stage
        if self.stage:
            # Stage specific configurations go back to the stage view
            url = reverse('projects_stage_view', args=(self.project.pk, self.stage.pk))
        else:
            # Project specific configurations go back to the project page
            url = self.project.get_absolute_url()

        return url

    def get_value(self):
        """Determine the proper value based on the data_type"""

        if self.data_type == self.BOOLEAN_TYPE:
            return self.value_boolean
        elif self.data_type == self.NUMBER_TYPE:
            return self.value_number
        else:
            return self.value

    def get_display_value(self):
        if self.sensitive_value:
            return "******"

        return self.get_value()


class Deployment(TrackingFields):
    """Archival record of an actual deployment, tracks:

    - Which user ran it
    - Stage it was on
    - Status
    - Fabric task that was run
    - The configuration used

    - Among other miscellaneous things
    """

    PENDING = 'pending'
    FAILED = 'failed'
    SUCCESS = 'success'

    STATUS = [(PENDING, 'Pending'), (FAILED, 'Failed'), (SUCCESS, 'Success')]

    user = models.ForeignKey(get_user_model())
    stage = models.ForeignKey(Stage)
    comments = models.TextField()
    status = models.CharField(choices=STATUS, max_length=10, default=PENDING)
    output = models.TextField(null=True, blank=True)
    task = models.ForeignKey('projects.Task')
    configuration = models.TextField(null=True, blank=True)

    # Managers
    objects = models.Manager()
    active_records = ActiveManager()
    # End Managers

    class Meta:
        ordering = ['-date_created']

    def __unicode__(self):
        return u'Deployment at {} status: {}'.format(self.date_created, self.get_status_display())


class Task(models.Model):
    name = models.CharField(max_length=255)
    times_used = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return u'{} ({})'.format(self.name, self.times_used)
