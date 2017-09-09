import json
from channels import Group
from channels.sessions import channel_session
from urlparse import parse_qs

from channels.auth import channel_session_user, channel_session_user_from_http

from channels.security.websockets import allowed_hosts_only

from channels import Channel

from room.play import process_entry, get_guessed_lyrics, get_prev_entries
from player.models import Player

# Connected to chat-messages
def msg_consumer(message):
    room_id = message.content['room_id']
    # Broadcast to listening sockets
    Group("chat-%s" % room_id).send({"text": json.dumps(message.content)})

@allowed_hosts_only
@channel_session_user_from_http
def ws_connect(message, room_id):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Parse the query string
    params = parse_qs(message.content["query_string"])
    if b"username" in params:
        # Set the username in the session
        message.channel_session["username"] = params[b"username"][0].decode("utf8")
        # Add the user to the room_name group
        Group("chat-%s" % room_id).add(message.reply_channel)
    else:
        # Close the connection.
        message.reply_channel.send({"close": True})

# Connected to websocket.receive
@channel_session_user
def ws_message(message, room_id):

    data = json.loads(message['text'])
    command = data['command']
    username = message.channel_session["username"]
    player = Player.objects.get(username=username)

    if command != 'join':
        entry = data['text']
        process_entry(entry, room_id, username)

    guessed_lyrics = get_guessed_lyrics(room_id)

    send_info = {
        "username": username,
        "nickname": player.nickname,
        "room_id": room_id,
        "guessed_lyrics": guessed_lyrics,
        "command": command,
    }

    if command != 'join':
        send_info['text'] = entry
    else:
        send_info['prev_entries'] = get_prev_entries(room_id)

    Channel('chat-messages').send(send_info)

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message, room_id):
    username = message.channel_session["username"]
    player = Player.objects.get(username=username)

    Channel('chat-messages').send({'command': 'leave', 'username': username, 'nickname': player.nickname, 'room_id': room_id})
    Group("chat-%s" % room_id).discard(message.reply_channel)