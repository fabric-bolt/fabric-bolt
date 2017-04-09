import subprocess
import ansiconv
import sys

from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from fabric_bolt.projects.models import Deployment
from fabric_bolt.projects.signals import deployment_finished
from fabric_bolt.projects.views import StageSubPageMixin

from .. import backend


class DeploymentOutputStream(StageSubPageMixin, View):
    """
    Deployment view does the heavy lifting of calling Fabric Task for a Project Stage
    """

    def output_stream_generator(self):
        if backend.get_task_details(self.project, self.object.task.name) is None:
            return

        try:
            process = subprocess.Popen(
                backend.build_command(self.project, self.object, self.request.session),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                executable=getattr(settings, 'SHELL', '/bin/bash'),
            )

            all_output = ''
            yield '<link rel="stylesheet" type="text/css" href="/static/css/console-style.css">'
            while True:
                nextline = process.stdout.readline()
                if nextline == '' and process.poll() is not None:
                    break

                all_output += nextline
                nextline = '<span class="output-line">{}</span>'.format(ansiconv.to_html(nextline))
                yield nextline + ' '*1024

                sys.stdout.flush()

            self.object.status = self.object.SUCCESS if process.returncode == 0 else self.object.FAILED

            yield '<span id="finished" style="display:none;">{}</span> {}'.format(self.object.status, ' '*1024)

            self.object.output = all_output
            self.object.save()

            deployment_finished.send(self.object, deployment_id=self.object.pk)

        except Exception as e:
            message = "An error occurred: " + e.message
            yield '<span class="output-line">{}</span>'.format(message) + ' '*1024
            yield '<span id="finished" style="display:none;">failed</span> {}'.format('*1024')

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            Deployment,
            stage=self.stage,
            pk=int(kwargs['pk']),
            status=Deployment.PENDING
        )
        resp = StreamingHttpResponse(self.output_stream_generator())
        return resp
