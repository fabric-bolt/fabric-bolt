from channels import Channel

from ..base import BaseTaskRunnerBackend


class ChannelsBackend(BaseTaskRunnerBackend):
    def get_detail_template(self):
        return 'task_runners/deployment_detail_channels.html'

    def pre_start_task(self, deployment, project, request):
        Channel("start_task").send({
            "deployment_id": deployment.id,
            "project_id": project.id,
            "session_key": request.session.session_key
        })
