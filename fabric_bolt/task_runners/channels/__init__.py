from ..base import BaseTaskRunnerBackend


channel_routing = {
    "websocket.connect": "fabric_bolt.task_runners.channels.consumers.ws_add",
    "websocket.keepalive": "fabric_bolt.task_runners.channels.consumers.ws_add",
    "websocket.receive": "fabric_bolt.task_runners.channels.consumers.ws_message",
    "websocket.disconnect": "fabric_bolt.task_runners.channels.consumers.ws_disconnect",
}


class ChannelsBackend(BaseTaskRunnerBackend):
    def get_detail_template(self):
        return 'task_runners/deployment_detail_channels.html'
