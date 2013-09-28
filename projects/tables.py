import django_tables2 as tables
import models


class ProjectTable(tables.Table):
    name = tables.LinkColumn('projects_project_update', kwargs={'pk': tables.A('pk')})

    class Meta:
        model = models.Project
        attrs = {"class": "table table-striped"}
        exclude = ('id',)