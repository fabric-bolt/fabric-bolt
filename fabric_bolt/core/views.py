import json
from datetime import timedelta

from django.db import connection
from django.db.models.aggregates import Count
from django.contrib import messages
from django.utils.timezone import now
from django.views.generic import TemplateView
from django.template.defaultfilters import date as format_date
from django.template.defaultfilters import time as format_time
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
        for window in LaunchWindow.objects.all():  # put this back once the migrations are created
            current_date = now()
            next_window = croniter(window.cron_format, current_date).get_next(current_date)
            if (next_window - current_date).seconds < 61:
                has_one_window = True
                continue

        if not has_one_window:
            messages.add_message(self.request, messages.ERROR,
                'No available Launch Windows! Next window on %s @ %s' % (format_date(next_window), format_time(next_window)))

        # Get the deployments and projects and bail if we don't have any
        deploys = list(Deployment.objects.order_by('date_created'))
        if len(deploys) == 0:
            return context

        projects = list(Project.objects.all())
        if len(projects) == 0:
            return context

        # Deployment Stats Data
        # Build pie chart data to show % projects deployed successfully
        items = [[item['status'], item['count']] for item in Deployment.objects.order_by('status').values('status').annotate(count=Count('id'))]
        context['pie_chart_data'] = json.dumps(items)

        # Deployment History Data
        # Get all projects with the days they were deployed and the count of the deploys on each day
        chart_data = []

        # If we're using postgres do this with one query, otherwise pound the db with the ORM.
        if connection.vendor == 'postgresql':
            # I couldn't figure out how to do this in the ORM with a Group By... here's a postgres version.
            # If you're smarter than me, and can fix this, please do.
            cursor = connection.cursor()
            cursor.execute("""
            SELECT project.name as project_name
            , date_trunc('day', deployment.date_created) as deploy_date
            , COUNT(date_trunc('day', deployment.date_created)) as deploy_count
            FROM "projects_project" as project
            LEFT JOIN "projects_stage" as stage ON ( project."id" = stage."project_id" )
            LEFT JOIN "projects_deployment" as deployment ON ( stage."id" = deployment."stage_id" )
            GROUP BY project.name, date_trunc('day', deployment.date_created)
            ORDER BY date_trunc('day', deployment.date_created), project.name
            """)

            rows = cursor.fetchall()

            # Get a distinct list of projects from our results
            project_names = []
            previous_project = ''
            for row in rows:
                if row[0] == previous_project:
                    continue
                previous_project = row[0]
                project_names.append(row[0])

            # Convert the sql results into a dictionary indexed by project and date (this makes the next step easier)
            project_deployment_data = {}
            for project in project_names:
                project_deployment_data[project] = {}
                for row in rows:
                    if project == row[0] and row[1] is not None:
                        project_deployment_data[project][row[1].strftime('%m/%d')] = row[2]

            # Build the google chart data using the project and date dictionary
            # We need an array for each day that has the deployment counts for each project
            deploy_day = None
            for row in rows:
                # If we have a project w/ no deployments, keep going
                if row[1] is None:
                    continue

                # If we already processed this day, keep going
                if row[1] == deploy_day:
                    continue

                # Process this day for each project
                deploy_day = row[1].strftime('%m/%d')
                daily_counts = [deploy_day]
                for project in project_names:
                    daily_counts.append(project_deployment_data[project].get(deploy_day, 0))

                chart_data.append(daily_counts)

            chart_data = [['Day'] + project_names] + chart_data

        else:
            # Get the date range for all the deployments ever done
            start_date = deploys[0].date_created
            end_date = deploys[len(deploys)-1].date_created

            # Step through each day and create an array of deployment counts from each project
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
                    # Nested ORM Call... not good.
                    data.append(Deployment.objects.select_related('stage').filter(stage__project_id=project.pk, date_created__range=range_).count())

                chart_data.append(data)

        context['chart_data'] = json.dumps(chart_data)

        return context