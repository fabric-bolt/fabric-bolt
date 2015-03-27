import django_tables2 as tables
from django_tables2.columns import LinkColumn

from fabric_bolt.core.mixins.tables import ActionsColumn, PaginateTable
from fabric_bolt.hosts.models import Host
from fabric_bolt.projects import models


class ProjectTable(PaginateTable):
    """Table used to display the projects

    Also provides actions to edit, view, and delete"""

    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-file"></i>', 'url': 'projects_project_view', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'View Project', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-pencil"></i>', 'url': 'projects_project_update', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Edit Project', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'projects_project_delete', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Delete Project', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-tags"></i>', 'url': 'projects_project_copy', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Copy Project', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    name = tables.LinkColumn('projects_project_view', kwargs={'pk': tables.A('pk')})
    deployments = tables.Column(accessor='get_deployment_count', verbose_name='# Deployments', orderable=False)

    class Meta:
        model = models.Project
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'name',
            'deployments',
        )


class ConfigurationTable(PaginateTable):
    """Table used to show the configurations

    Also provides actions to edit and delete"""

    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-pencil"></i>', 'url': 'projects_configuration_update', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Edit Configuration', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'projects_configuration_delete', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Delete Configuration', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    key = tables.LinkColumn('projects_configuration_update', kwargs={'pk': tables.A('pk')})
    value = tables.Column(accessor='get_display_value', orderable=False)

    # Clean up the labels a little
    task_argument = tables.BooleanColumn(verbose_name="Argument?",)
    prompt_me_for_input = tables.BooleanColumn(verbose_name="Prompt?",)
    sensitive_value = tables.BooleanColumn(verbose_name="Sensitive?",)

    class Meta:
        model = models.Configuration
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'key',
            'value',
            'task_argument',
            'prompt_me_for_input',
            'sensitive_value',
        )


class StageTable(PaginateTable):
    """Table used to show the stages

    Also provides actions for view, edit, and delete"""

    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-file"></i>', 'url': 'projects_stage_view', 'args': [tables.A('project_id'), tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'View Stage Details', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-pencil"></i>', 'url': 'projects_stage_update', 'args': [tables.A('project_id'), tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Edit Stage', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'projects_stage_delete', 'args': [tables.A('project_id'), tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Delete Stage', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    hosts = tables.Column(accessor='host_count', verbose_name='# Hosts')
    deployments = tables.Column(accessor='deployment_count', verbose_name='# Deployments', order_by='deployment_count')

    class Meta:
        model = models.Stage
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'name',
            'hosts',
            'deployments',
            'actions',
        )


class DeploymentTable(PaginateTable):
    """Table used to show the deployments

    Also provides actions to view individual deployment"""

    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-file"></i>', 'url': 'projects_deployment_detail', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'View Deployment Details', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    task_name = tables.Column(accessor='task.name', verbose_name='Task')

    user = LinkColumn('accounts_user_view',
                      accessor='user.email',
                      args=[tables.A('pk')],
                      attrs={'data-toggle': 'tooltip',
                             'title': 'View user details',
                             'data-delay': '{ "show": 300, "hide": 0 }'},
                      verbose_name=('Deployer'))

    # Prettify the status
    status = tables.TemplateColumn('<span style="font-size:13px;" class="label label-{% if record.status == "success" %}success{% elif record.status == "failed" %}danger{% else %}info{% endif %}"><i class="glyphicon glyphicon-{% if record.status == "success" %}ok{% elif record.status == "failed" %}warning-sign{% else %}time{% endif %}"></i> &#160;{{ record.get_status_display }}</span>')

    class Meta:
        model = models.Deployment
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'date_created',
            'user',
            'stage',
            'task_name',
            'status',
            'actions',
        )


class StageHostTable(PaginateTable):
    """This table lists the Stage->Host through table records

    Also provides actions to view and un-map the host to the stage
    """

    def __init__(self, *args, **kwargs):
        stage_id = kwargs.pop('stage_id')

        self.base_columns['actions'] = ActionsColumn([
            {'title': '<i class="glyphicon glyphicon-file"></i>', 'url': 'hosts_host_detail', 'args': [tables.A('pk')],
             'attrs':{'data-toggle': 'tooltip', 'title': 'View Host', 'data-delay': '{ "show": 300, "hide": 0 }'}},
            {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'projects_stage_unmaphost', 'args': [stage_id, tables.A('pk'),],
             'attrs':{'data-toggle': 'tooltip', 'title': 'Remove Host from Stage', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        ], delimiter='&#160;&#160;&#160;')

        super(StageHostTable, self).__init__(*args, **kwargs)

    class Meta:
        model = Host
        attrs = {"class": "table table-striped"}
        exclude = ('id',)
        sequence = fields = (
            'name',
            'actions'
        )