# from channels import route_class
# from codenerix_pos.consumers import POSConsumer
from channels.routing import route
from codenerix_pos.consumers import ws_message

# channel_routing = [
#    route_class(POSConsumer, path=r"^/codenerix_pos/"),
# ]
channel_routing = [
    route("websocket.receive", ws_message),
]
