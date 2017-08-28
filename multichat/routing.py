from channels.routing import route
# from multichat.consumers import ws_add, ws_message, ws_disconnect
from multichat.consumers import ws_connect, ws_message, ws_disconnect, msg_consumer

# channel_routing = [
#     # route("http.request", "multichat.consumers.http_consumer"),
    
#     route("websocket.connect", ws_connect),
#     route("websocket.receive", ws_message),
#     route("websocket.disconnect", ws_disconnect),
# ]


from django.conf.urls import include
http_routing = [
    # route("http.request", poll_consumer, path=r"^/poll/$", method=r"^POST$"),
]

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.receive", ws_message, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("chat-messages", msg_consumer)
]

# routing = [
#     # You can use a string import path as the first argument as well.
#     include(channel_routing, path=r"^/chat"),
#     include(http_routing),
# ]



# socket = new WebSocket("ws://" + window.location.host + "/name/?username=abc/");
# socket.onmessage = function(e) {
#     alert(e.data);
# }
# socket.onopen = function() {
#     socket.send("hello world");
# }
# // Call onopen directly if socket is already open
# if (socket.readyState == WebSocket.OPEN) socket.onopen();