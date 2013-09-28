import django_tables2 as tables
import models
from core.mixins.tables import ActionsColumn


class HostTable(tables.Table):
    actions = ActionsColumn([
        {'title': '<i class="glyphicon glyphicon-pencil"></i>', 'url': 'hosts_host_update', 'args': [tables.A('pk')],
         'attrs':{'data-toggle': 'tooltip', 'title': 'Edit Host'}},
    ])

    class Meta:
        model = models.Host
        attrs = {"class": "table table-striped"}
        exclude = ('id',)