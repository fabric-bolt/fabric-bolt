from datetime import timedelta
import json

from django.views.generic import TemplateView
from django.db.models.aggregates import Count

from fabric_bolt.projects.models import Project, Deployment


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):

        context = super(Dashboard, self).get_context_data(**kwargs)

        deploys = Deployment.objects.order_by('date_created')

        if deploys.count() == 0:
            return context

        start_date = deploys[0].date_created
        end_date = deploys[deploys.count()-1].date_created

        chart_data = []

        projects = Project.objects.all()

        if projects.count():

            for day in range(-1, (end_date.date() - start_date.date()).days + 1):
                date = start_date + timedelta(days=day)
                if day == -1:
                    data = ['Day']
                else:
                    data = [date.strftime('%m/%d')]

                for project in projects:
                    if day == -1:
                        data.append(project.name)
                        continue

                    range_ = (date.date(), date.date() + timedelta(days=1))
                    data.append(Deployment.objects.filter(stage__project_id=project.pk, date_created__range=range_).count())

                chart_data.append(data)

            context['chart_data'] = json.dumps(chart_data)

        items = [[item['status'], item['count']] for item in Deployment.objects.order_by('status').values('status').annotate(count=Count('id'))]

        context['pie_chart_data'] = json.dumps(items)

        return context