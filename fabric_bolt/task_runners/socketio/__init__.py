from ..base import BaseTaskRunnerBackend


class SocketIOBackend(BaseTaskRunnerBackend):
    def __init__(self):
        from . import sockets

    def get_detail_template(self):
        return 'task_runners/deployment_detail_socketio.html'
