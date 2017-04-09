from channels.routing import route

from . import consumers

channel_routing = [
    route("websocket.connect", consumers.ws_connect),
    # route("websocket.receive", consumers.ws_receive),
    route("websocket.disconnect", consumers.ws_disconnect),
    route("start_task", consumers.start_task),
]
