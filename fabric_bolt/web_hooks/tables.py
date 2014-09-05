import django_tables2 as tables

from fabric_bolt.core.mixins.tables import ActionsColumn, PaginateTable

from fabric_bolt.web_hooks import models


class HookTable(PaginateTable):
    """Table used to show the configurations

    Also provides actions to edit and delete"""

    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-pencil"></i>', 'url': 'hooks_hook_update', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Edit Hook', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'hooks_hook_delete', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Delete Hook', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    class Meta:
        model = models.Hook
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'project',
            'url',
        )