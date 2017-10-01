from channels.routing import route
from multichat.consumers import ws_connect, ws_message, ws_disconnect, msg_consumer

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/(?P<game_id>[0-9]+)/$"),
    route("websocket.receive", ws_message, path=r"^/(?P<game_id>[0-9]+)/$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/(?P<game_id>[0-9]+)/$"),
    route("chat-messages", msg_consumer)
]