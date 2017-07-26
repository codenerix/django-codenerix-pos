from channels import route_class
from codenerix_pos.consumers import POSConsumer
# from channels.routing import route
# from codenerix_pos.consumers import ws_message, ws_connect, ws_disconnect

channel_routing = [
    route_class(POSConsumer, path=r"^/codenerix_pos/"),
]
# channel_routing = [
#    route("websocket.connect", ws_connect, path=r"^\/codenerix_pos\/(?P<uid>[a-zA-Z0-9_]+)$"),
#    route("websocket.receive", ws_message, path=r"^/codenerix_pos/(?P<uid>[a-zA-Z0-9_]+)$"),
#    route("websocket.disconnect", ws_disconnect, path=r"^/codenerix_pos/(?P<uid>[a-zA-Z0-9_]+)$"),
# ]
