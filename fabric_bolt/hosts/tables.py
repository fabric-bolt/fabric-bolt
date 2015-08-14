import django_tables2 as tables

from fabric_bolt.hosts import models
from fabric_bolt.core.mixins.tables import ActionsColumn, PaginateTable


class HostTable(PaginateTable):
    name = tables.LinkColumn('hosts_host_detail', args=[tables.A('pk')], verbose_name='Name')
    alias = tables.Column(verbose_name='Alias')
    actions = ActionsColumn(
        [
            {
                'title': '<i class="glyphicon glyphicon-pencil"></i>',
                'url': 'hosts_host_update',
                'args': [tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'Edit Host', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
            {
                'title': '<i class="glyphicon glyphicon-trash"></i>',
                'url': 'hosts_host_delete',
                'args': [tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'Delete Host', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
        ],
        delimiter='&#160;&#160;&#160;'
    )

    class Meta:
        model = models.Host
        attrs = {"class": "table table-striped"}
        fields = ('name', 'alias', 'actions')
