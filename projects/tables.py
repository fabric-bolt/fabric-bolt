import django_tables2 as tables

from core.mixins.tables import ActionsColumn, PaginateTable

from hosts.tables import HostTable

from . import models



class ProjectTable(PaginateTable):
    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-file"></i>', 'url': 'projects_project_view', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'View Project', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-pencil"></i>', 'url': 'projects_project_update', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Edit Project', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'projects_project_delete', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Delete Project', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    name = tables.LinkColumn('projects_project_view', kwargs={'pk': tables.A('pk')})

    class Meta:
        model = models.Project
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'name',
            'type',
            'number_of_deployments',
        )


class ConfigurationTable(PaginateTable):

    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-pencil"></i>', 'url': 'projects_configuration_update', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Edit Configuration', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'projects_configuration_delete', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Delete Configuration', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    key = tables.LinkColumn('projects_configuration_update', kwargs={'pk': tables.A('pk')})
    value = tables.Column(accessor='get_value', orderable=False)
    prompt_me_for_input = tables.BooleanColumn(verbose_name="Prompt?",)
    sensitive_value = tables.BooleanColumn(verbose_name="Sensitive?",)

    class Meta:
        model = models.Configuration
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'key',
            'value',
            'prompt_me_for_input',
            'sensitive_value',
        )


class StageTable(PaginateTable):
    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-file"></i>', 'url': 'projects_stage_view', 'args': [tables.A('project.pk'), tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'View Stage Details', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-pencil"></i>', 'url': 'projects_stage_update', 'args': [tables.A('project.pk'), tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Edit Stage', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'projects_stage_delete', 'args': [tables.A('project.pk'), tables.A('pk')],
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
    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-file"></i>', 'url': 'projects_deployment_detail', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'View Deployment Details', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    task_name = tables.Column(accessor='task.name', verbose_name='Task')
    status = tables.TemplateColumn('<span class="label label-{% if record.status == "success" %}success{% elif record.status == "failed" %}danger{% else %}info{% endif %}">{{ record.get_status_display }}</span>')

    class Meta:
        model = models.Deployment
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'date_created',
            'stage',
            'task_name',
            'status',
            'actions'
        )


class StageHostTable(HostTable):

    def __init__(self):
        super(StageHostTable, self).__init__()

        self.actions = ActionsColumn([
            {'title': '<i class="glyphicon glyphicon-file"></i>', 'url': 'hosts_host_detail', 'args': [tables.A('pk')],
             'attrs':{'data-toggle': 'tooltip', 'title': 'View Host', 'data-delay': '{ "show": 300, "hide": 0 }'}},
            {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'projects_stage_unmaphost', 'args': [tables.A('pk')],
             'attrs':{'data-toggle': 'tooltip', 'title': 'Unmap Host', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        ], delimiter='&#160;&#160;&#160;')