import django_tables2 as tables

import models
from core.mixins.tables import ActionsColumn


class ProjectTable(tables.Table):
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


class ConfigurationTable(tables.Table):

    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-pencil"></i>', 'url': 'projects_configuration_update', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Edit Configuration', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'projects_configuration_delete', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Delete Configuration', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    key = tables.LinkColumn('projects_configuration_update', kwargs={'pk': tables.A('pk')})

    class Meta:
        model = models.Configuration
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'key',
            'value',
        )


class DeploymentTable(tables.Table):
    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-file"></i>', 'url': 'projects_deployment_detail', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'View Deployment Details', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    task_name = tables.Column(accessor='task.name', verbose_name='Task')

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