from channels import route_class
from codenerix_pos.consumers import POSConsumer

channel_routing = [
    route_class(POSConsumer, path=r"^/codenerix_pos/"),
]
