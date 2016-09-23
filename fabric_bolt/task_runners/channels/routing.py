from channels.routing import route

channel_routing = [
    route("websocket.connect", "fabric_bolt.task_runners.channels.consumers.ws_connect"),
    route("websocket.disconnect", "fabric_bolt.task_runners.channels.consumers.ws_disconnect"),
    route("start_task", "fabric_bolt.task_runners.channels.consumers.start_task"),
]
