# from django.http import HttpResponse
# from channels.handler import AsgiHandler

# def http_consumer(message):
#     # Make standard HTTP response - access ASGI path attribute directly
#     response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
#     # Encode that response into message format (ASGI)
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)




# from channels import Group

# # Connected to websocket.connect
# def ws_connect(message):
#     # Accept the connection
#     message.reply_channel.send({"accept": True})
#     # Add to the chat group
#     Group("chat").add(message.reply_channel)

# # Connected to websocket.receive
# def ws_message(message):
#     Group("chat").send({
#         "text": "[user] %s" % message.content['text'],
#     })

# # Connected to websocket.disconnect
# def ws_disconnect(message):
#     Group("chat").discard(message.reply_channel)


import json
from channels import Group
from channels.sessions import channel_session
from urlparse import parse_qs

from channels.auth import channel_session_user, channel_session_user_from_http

from channels.security.websockets import allowed_hosts_only

# Connected to websocket.connect
# @channel_session


@allowed_hosts_only
@channel_session_user_from_http
def ws_connect(message, room_name):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Parse the query string
    params = parse_qs(message.content["query_string"])
    if b"username" in params:
        # Set the username in the session
        message.channel_session["username"] = params[b"username"][0].decode("utf8")
        # Add the user to the room_name group
        Group("chat-%s" % room_name).add(message.reply_channel)
    else:
        # Close the connection.
        message.reply_channel.send({"close": True})

# Connected to websocket.receive
# @channel_session

@channel_session_user
def ws_message(message, room_name):
    Group("chat-%s" % room_name).send({
        "text": json.dumps({
            "text": message["text"],
            "username": message.channel_session["username"],
        }),
    })

# Connected to websocket.disconnect
# @channel_session

@channel_session_user
# def ws_disconnect(message):
def ws_disconnect(message, room_name):
    Group("chat-%s" % room_name).discard(message.reply_channel)