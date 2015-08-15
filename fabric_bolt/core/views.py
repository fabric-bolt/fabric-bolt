from datetime import timedelta, datetime

from django.utils import timezone
from django.db.models.aggregates import Count
from django.contrib import messages
from django.views.generic import TemplateView
from django.template.defaultfilters import date as format_date
from django.template.defaultfilters import time as format_time

from graphos.renderers.gchart import PieChart, LineChart
from graphos.sources.simple import SimpleDataSource
from croniter import croniter

from fabric_bolt.launch_window.models import LaunchWindow
from fabric_bolt.projects.models import Project, Deployment


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):

        context = super(Dashboard, self).get_context_data(**kwargs)

        # Warn the user if we don't have an available Launch Window
        has_one_window = False
        next_window = None
        launch_windows = LaunchWindow.objects.all()

        for window in launch_windows:
            current_date = datetime.now()

            next_window = croniter(window.cron_format, current_date).get_next(datetime)
            if (next_window - datetime.now()).seconds < 61:
                has_one_window = True
                break

        if not has_one_window and launch_windows.exists():
            messages.add_message(self.request, messages.ERROR,
                'No available Launch Windows! Next window on %s @ %s' % (format_date(next_window), format_time(next_window)))

        # Deployment Stats Data
        # Build pie chart data to show % projects deployed successfully
        deployments = Deployment.active_records.order_by('status').values('status').annotate(count=Count('id'))
        items = [['string', 'number']] + [
            [item['status'], item['count']] for item in deployments
        ]
        context['pie_chart'] = PieChart(SimpleDataSource(items), width='100%', height=300, options={'title': ''})

        # Deployment History Data
        # Get all projects with the days they were deployed and the count of the deploys on each day
        chart_data = []

        projects = list(Project.active_records.all())
        if len(projects) == 0:
            return context

        deploys = list(Deployment.objects.select_related('stage').order_by('date_created'))

        # Get the date range for all the deployments ever done
        start_date = (timezone.now() - timedelta(days=60)).date()
        end_date = timezone.now().date()

        # Step through each day and create an array of deployment counts from each project
        # this would be much easier if we could aggregate by day.
        # once we can use django 1.7, we could write a __date transform. Then it would work.
        for day in range(-1, (end_date - start_date).days + 1):
            date = start_date + timedelta(days=day)
            if day == -1:
                data = ['Day']
            else:
                data = [date.strftime('%m/%d')]

            for project in projects:
                if day == -1:
                    data.append(project.name)
                    continue

                count = 0
                for d in deploys:
                    if d.stage.project_id == project.pk and d.date_created.date() == date:
                        count += 1

                data.append(count)

            chart_data.append(data)

        context['line_chart'] = LineChart(SimpleDataSource(chart_data), width='100%', height=300, options={'title': ''})

        return context