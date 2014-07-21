import django_tables2 as tables

from fabric_bolt.launch_window import models
from fabric_bolt.core.mixins.tables import ActionsColumn, PaginateTable


class LaunchWindowTable(PaginateTable):
    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-file"></i>', 'url': 'launch_window_launchwindow_detail', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'View Launch Window', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-pencil"></i>', 'url': 'launch_window_launchwindow_update', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Edit Launch Window', 'data-delay': '{ "show": 300, "hide": 0 }'}},
        {'title': '<i class="glyphicon glyphicon-trash"></i>', 'url': 'launch_window_launchwindow_delete', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Delete Launch Window', 'data-delay': '{ "show": 300, "hide": 0 }'}},
    ], delimiter='&#160;&#160;&#160;')

    class Meta:
        model = models.LaunchWindow
        attrs = {"class": "table table-striped"}
        exclude = ('id',)