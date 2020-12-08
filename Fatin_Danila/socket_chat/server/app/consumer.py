import hashlib
import socket
from secrets import token_hex

from app.config import ROOM_HISTORY_LIMIT, SERVER_HOST, SERVER_PORT, SERVER_SIGNATURE
from app.helpers import list_commands, get_input_data, get_output_data
from app.helpers.decorators import event, sign_response


users_by_logins = {}


class User:
    def __init__(self, address, login, password_hash):
        self.address = address
        self.login = login
        self.password_hash = password_hash
        self.token = None
        self.subscribed_rooms = []
        self.current_room = None

    def go_online(self):
        for room in self.subscribed_rooms:
            room.subscribers_by_login[self.login].address = self.address

    def go_offline(self):
        for room in self.subscribed_rooms:
            room.subscribers_by_login[self.login].address = None


class Subscriber:
    def __init__(self, login, room_nickname):
        self.login = login
        self.room_nickname = room_nickname


class Message:
    def __init__(self, sender_login, message):
        self.sender_login = sender_login
        self.text = message


class Room:
    def __init__(self, title):
        self.title = title
        self.subscribers_by_login = {}
        self.subscribers_nicknames = []
        self.messages = []

    @event('message_history')
    def show_history(self):
        history = []
        for message in self.messages:
            author = self.subscribers_by_login[message.sender_login]
            history.append({
                'author': author.room_nickname,
                'message': message.text,
                'room': self.title,
                'current': True,
            })

        return history

    @event('input_message')
    def publish_message(self, message, sender):
        if len(self.messages) >= ROOM_HISTORY_LIMIT:
            self.messages.pop(0)
        new_message = Message(sender.login, message)
        self.messages.append(new_message)

        sender = self.subscribers_by_login[sender.login]
        messages = []
        for login, subscriber in self.subscribers_by_login.items():
            if subscriber != sender:
                user = users_by_logins[login]
                messages.append({
                    'author': sender.room_nickname,
                    'message': message,
                    'address': subscriber.address,
                    'room': self.title,
                    'current': user.current_room == self.title,
                })

        return messages


class Server:
    server_address = (SERVER_HOST, SERVER_PORT)

    def __init__(self):
        self.users_by_tokens = {}
        self.rooms_by_titles = {}

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.server_address)
            s.listen()
            conn, address = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    data = get_input_data(data)
                    for res in data:
                        response = self.get_response(res, address)
                        if response is None:
                            return

                        if isinstance(response, list):
                            for message in response:
                                message_address = message.get('address', address)
                                message = get_output_data(message)
                                conn.sendto(message, message_address)
                        else:
                            response = get_output_data(response)
                            conn.sendall(response)

    @event('base_event')
    @sign_response(SERVER_SIGNATURE)
    def get_response(self, data, address):
        user = self.identify_user(data)
        if user is None:
            if data.get('command') == '/help':
                return self.handle_command(data['command'], data, None)
            if data.get('command') == '/create_profile':
                return self.register_user(data['login'], data['password'], address)
            if data.get('command') == '/auth':
                return self.auth_user(data['login'], data['password'], address)

            return {'message': 'You need to log in to continue. Use /create_profile or /auth'}

        message, command = data.get('message'), data.get('command')
        if message is not None:
            return self.handle_message(message, user)

        if command is not None:
            return self.handle_command(command, data, user)

        return {'message': 'Unexpected actions'}

    def identify_user(self, data):
        token = data.get('token')
        if token is not None:
            return self.users_by_tokens.get(token)

        return None

    @event('register_user')
    def register_user(self, login, password, address):
        if users_by_logins.get(login) is not None:
            return {'message': 'Sorry, this login is already taken, pick another one.'}

        password_hash = hashlib.md5(password.encode()).hexdigest()
        token = token_hex(16)
        new_user = User(address, login, password_hash)
        new_user.token = token
        users_by_logins[login] = new_user
        self.users_by_tokens[token] = new_user

        return {'message': 'Registration successful', 'token': token}

    @event('auth_user')
    def auth_user(self, login, password, address):
        user = users_by_logins.get(login)
        if user is None:
            return {'message': 'Login and password do not match'}
        password_hash = hashlib.md5(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            return {'message': 'Login and password do not match'}
        else:
            token = token_hex(16)
            user.token = token
            user.address = address
            user.go_online()
            self.users_by_tokens[token] = user

            return {'message': 'Authentication successful', 'token': token}

    def handle_message(self, message, user):
        if user.current_room is None:
            return {'message': 'You have to join or create a room to send messages'}

        room = self.rooms_by_titles[user.current_room]

        return room.publish_message(message, user)

    def handle_command(self, command, data, user):
        if command == '/create_profile':
            return {'message': 'You are currently logged in. Logout if you want to create new profile'}

        if command == '/auth':
            return {'message': 'You are currently logged in. Logout if you want to login to another profile'}

        if command == '/create_room':
            room_title = data['room_title']
            if self.rooms_by_titles.get(room_title) is not None:
                return {'message': 'Such room already exists'}

            nickname_for_room = data['nickname_for_room']
            new_room = Room(room_title)
            self.rooms_by_titles[room_title] = new_room
            new_room.subscribers_by_login[user.login] = Subscriber(user.login, nickname_for_room)
            user.subscribed_rooms.append(new_room)

            return {'message': 'Room created'}

        if command == '/subscribe':
            room_title = data['room_title']
            room = self.rooms_by_titles.get(room_title)
            if room is None:
                return {'message': 'There is no such room'}

            nickname_for_room = data['nickname_for_room']
            if nickname_for_room in room.subscribers_nicknames:
                return {'message': 'Sorry, this nickname is already taken in the room'}

            room.subscribers_by_login[user.login] = Subscriber(user.login, nickname_for_room)
            user.subscribed_rooms.append(room)

            return {'message': 'Subscribed to room'}

        if command == '/join':
            room_title = data['room_title']
            room = self.rooms_by_titles.get(room_title)
            if room is None:
                return {'message': 'There is no such room'}

            if room.subscribers_by_login.get(user.login) is None:
                return {'message': 'In order to join the room you firstly have to subscribe to it'}

            user.current_room = room.title
            room_history = room.show_history()
            message = [{'message': 'Room joined', 'room': None, 'current': False}] + room_history

            return message

        if command == '/rooms':
            which_rooms = data.get('which_rooms')
            if which_rooms == '--my':
                rooms = [f' - {room.title}' for room in user.subscribed_rooms]
                message = '\n'.join(rooms) if rooms else "You haven't subscribed to any rooms"
            elif which_rooms == '--current':
                message = f'\n - {user.current_room}' if user.current_room else "You are not in room"
            elif which_rooms is None:
                rooms = [f' - {room_title}' for room_title in self.rooms_by_titles.keys()]
                message = '\n'.join(rooms) if rooms else 'There are no rooms'
            else:
                message = 'Unknown parameter'

            return {'message': message}

        if command == '/quit':
            if user.current_room is None:
                return {'message': 'You are not in room'}

            user.current_room = None
            return {'message': 'Quit room'}

        if command == '/logout':
            del self.users_by_tokens[user.token]
            user.token = None
            user.current_room = None
            user.go_offline()
            return {'message': 'Logout'}

        if command == '/shutdown':
            user.go_offline()
            return {'message': 'Shutdown'}

        if command == '/poweron':
            user.go_online()
            return {'message': 'Power on'}

        if command == '/help':
            return {'message': list_commands()}

        return {'message': list_commands()}


def run_server():
    server = Server()
    server.run()


if __name__ == '__main':
    run_server()

