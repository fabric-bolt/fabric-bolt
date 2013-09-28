import django_tables2 as tables
import models


class ProjectTable(tables.Table):
    name = tables.LinkColumn('projects_project_view', kwargs={'pk': tables.A('pk')})

    class Meta:
        model = models.Project
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'name',
            'type',
            'number_of_deployments',
        )