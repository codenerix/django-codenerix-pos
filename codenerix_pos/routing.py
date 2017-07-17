from channels import route
from codenerix_pos import consumers

channel_routing = [
    # Wire up websocket channels to our consumers:
    route("http.request", consumers.http_consumer),
    route("websocket.connect", consumers.ws_connect),
    route("websocket.receive", consumers.ws_receive),
    route("websocket.disconnect", consumers.ws_receive),
]
