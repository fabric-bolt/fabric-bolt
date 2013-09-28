import django_tables2 as tables
import models


class HostTable(tables.Table):
    name = tables.LinkColumn('hosts_host_update', kwargs={'pk': tables.A('pk')})

    class Meta:
        model = models.Host
        attrs = {"class": "table table-striped"}
        exclude = ('id',)