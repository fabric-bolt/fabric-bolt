import django_tables2 as tables
from django_tables2.columns import LinkColumn

from fabric_bolt.core.mixins.tables import ActionsColumn, PaginateTable, BooleanColumn
from fabric_bolt.hosts.models import Host
from fabric_bolt.projects import models


class ProjectTable(PaginateTable):
    """Table used to display the projects

    Also provides actions to edit, view, and delete"""

    actions = ActionsColumn(
        [
            {
                'title': '<i class="glyphicon glyphicon-pencil"></i>',
                'url': 'projects_project_update',
                'args': [tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'Edit Project', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
            {
                'title': '<i class="glyphicon glyphicon-trash"></i>',
                'url': 'projects_project_delete',
                'args': [tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'Delete Project', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
            {
                'title': '<i class="glyphicon glyphicon-duplicate"></i>',
                'url': 'projects_project_copy',
                'args': [tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'Copy Project', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
        ],
        delimiter='&#160;&#160;&#160;'
    )

    name = tables.LinkColumn('projects_project_view', kwargs={'pk': tables.A('pk')}, verbose_name='Name')
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

    actions = ActionsColumn(
        [
            {
                'title': '<i class="glyphicon glyphicon-pencil"></i>',
                'url': 'projects_configuration_update',
                'args': [tables.A('project_id'), tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'Edit Configuration', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
            {
                'title': '<i class="glyphicon glyphicon-trash"></i>',
                'url': 'projects_configuration_delete',
                'args': [tables.A('project_id'), tables.A('pk')],
                'attrs':{'data-toggle': 'tooltip', 'title': 'Delete Configuration', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
        ],
        delimiter='&#160;&#160;&#160;'
    )

    key = tables.LinkColumn(
        'projects_configuration_update',
        kwargs={'project_id': tables.A('project_id'), 'pk': tables.A('pk')},
        verbose_name='Key'
    )
    value = tables.Column(accessor='get_display_value', orderable=False)

    # Clean up the labels a little
    task_argument = BooleanColumn(verbose_name="Argument?",)
    prompt_me_for_input = BooleanColumn(verbose_name="Prompt?",)
    sensitive_value = BooleanColumn(verbose_name="Sensitive?",)

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

    actions = ActionsColumn(
        [
            {
                'title': '<i class="glyphicon glyphicon-pencil"></i>',
                'url': 'projects_stage_update',
                'args': [tables.A('project_id'), tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'Edit Stage', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
            {
                'title': '<i class="glyphicon glyphicon-trash"></i>',
                'url': 'projects_stage_delete',
                'args': [tables.A('project_id'), tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'Delete Stage', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
        ],
        delimiter='&#160;&#160;&#160;'
    )

    name = tables.LinkColumn('projects_stage_view', args=[tables.A('project_id'), tables.A('pk')], verbose_name='Name')
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

    date_created = tables.Column(verbose_name='Created')

    user = LinkColumn(
        'accounts_user_view',
        accessor='user.email',
        args=[tables.A('user.pk')],
        attrs={'data-toggle': 'tooltip','title': 'View user details','data-delay': '{ "show": 300, "hide": 0 }'},
        verbose_name='Deployer'
    )

    stage = tables.Column(verbose_name='Stage')

    task_name = tables.Column(accessor='task.name', verbose_name='Task')

    status = tables.TemplateColumn(
        template_name='projects/pieces/deployment_status_column.html',
        verbose_name='Status'
    )

    actions = ActionsColumn(
        [
            {
                'title': '<i class="glyphicon glyphicon-file"></i>',
                'url': 'projects_deployment_detail',
                'args': [tables.A('stage.project_id'), tables.A('stage_id'), tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'View Deployment Details', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
        ],
        delimiter='&#160;&#160;&#160;'
    )

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


class RecentDeploymentsTable(tables.Table):
    """Table used to show the recent deployments of a user"""
    project = tables.Column(accessor='stage.project.name', verbose_name='Project', orderable=False)
    stage = tables.Column(accessor='stage.name', verbose_name='Stage', orderable=False)
    task_name = tables.Column(accessor='task.name', verbose_name='Task', orderable=False)
    status = tables.TemplateColumn(
        template_name='projects/pieces/recentdeployment_status_column.html',
        verbose_name='Status'
    )

    actions = ActionsColumn(
        [
            {
                'title': '<i class="glyphicon glyphicon-file"></i>',
                'url': 'projects_deployment_detail',
                'args': [tables.A('stage.project_id'), tables.A('stage_id'), tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'View Deployment Details', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
        ],
        delimiter='&#160;&#160;&#160;'
    )

    class Meta:
        model = models.Deployment
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'project',
            'stage',
            'task_name',
            'status',
            'actions',
        )
        empty_text = "This user hasn't made any deployments."


class StageHostTable(PaginateTable):
    """This table lists the Stage->Host through table records

    Also provides actions to view and un-map the host to the stage
    """

    name = tables.LinkColumn('hosts_host_detail', args=(tables.A('pk'),), verbose_name='Name')

    def __init__(self, *args, **kwargs):
        stage_id = kwargs.pop('stage_id')
        project_id = kwargs.pop('project_id')

        self.base_columns['actions'] = ActionsColumn(
            [
                {
                    'title': '<i class="glyphicon glyphicon-trash"></i>',
                    'url': 'projects_stage_unmaphost',
                    'args': [project_id, stage_id, tables.A('pk')],
                    'attrs': {'data-toggle': 'tooltip', 'title': 'Remove Host from Stage', 'data-delay': '{ "show": 300, "hide": 0 }'}
                },
            ],
            delimiter='&#160;&#160;&#160;'
        )

        super(StageHostTable, self).__init__(*args, **kwargs)

    class Meta:
        model = Host
        attrs = {"class": "table table-striped"}
        exclude = ('id',)
        sequence = fields = (
            'name',
            'actions'
        )
