import json
from channels import Group
from channels.sessions import channel_session
from urlparse import parse_qs

from channels.auth import channel_session_user, channel_session_user_from_http

from channels.security.websockets import allowed_hosts_only

from channels import Channel

from room.play import process_entry, get_guessed_lyrics, get_prev_entries, convert_guessed_lyrics_to_html, convert_prev_entries_to_html
from player.models import Player
from room.play import save_activity_log, get_connected_users

# Connected to chat-messages
def msg_consumer(message):
    game_id = message.content['game_id']
    # Broadcast to listening sockets
    Group("chat-%s" % game_id).send({"text": json.dumps(message.content)})

@allowed_hosts_only
@channel_session_user_from_http
def ws_connect(message, game_id):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Parse the query string
    get_connected_users(game_id)
    params = parse_qs(message.content["query_string"])
    if b"user_id" in params:
        # Set the username in the session
        message.channel_session["user_id"] = params[b"user_id"][0]
        # Add the user to the room_name group
        Group("chat-%s" % game_id).add(message.reply_channel)
    else:
        # Close the connection.
        message.reply_channel.send({"close": True})

# Connected to websocket.receive
@channel_session_user
def ws_message(message, game_id):

    data = json.loads(message['text'])
    command = data['command']
    user_id = message.channel_session["user_id"]
    player = Player.objects.get(id=user_id)

    send_info = {
        "user_id": user_id,
        "nickname": player.nickname,
        "game_id": game_id,
        "command": command,
    }

    if command == 'guess':
        word = data['text']
        entry_result = process_entry(word, game_id, user_id)

        if entry_result is None:
            return

        send_info['positions_words'] = entry_result['positions_words']
        send_info['exist'] = entry_result['exist']
        send_info['word'] = word

    if command == 'join':

        lyrics_lines = get_guessed_lyrics(game_id)
        lyrics_lines_html = convert_guessed_lyrics_to_html(lyrics_lines)

        active_players = get_connected_users(game_id)

        prev_entries = get_prev_entries(game_id)
        prev_entries_html = convert_prev_entries_to_html(prev_entries)

        send_info['active_players'] = active_players
        send_info['prev_entries_html'] = prev_entries_html
        send_info['lyrics_html'] = lyrics_lines_html

    if command != 'guess':
        save_activity_log(name=command, user_id=user_id, game_id=game_id)

    Channel('chat-messages').send(send_info)

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message, game_id):
    user_id = message.channel_session["user_id"]
    player = Player.objects.get(id=user_id)

    save_activity_log(name='leave', user_id=user_id, game_id=game_id)
    Channel('chat-messages').send({'command': 'leave', 'user_id': user_id, 'nickname': player.nickname, 'game_id': game_id})
    Group("chat-%s" % game_id).discard(message.reply_channel)