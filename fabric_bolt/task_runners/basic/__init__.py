from django.conf.urls import url

from ..base import BaseTaskRunnerBackend


class BasicStreamBackend(BaseTaskRunnerBackend):
    def get_detail_template(self):
        return 'task_runners/deployment_detail_basic.html'

    def get_urls(self):
        from .views import DeploymentOutputStream

        return [
            url(r'^output/$', DeploymentOutputStream.as_view(), name='projects_deployment_output'),
        ]
