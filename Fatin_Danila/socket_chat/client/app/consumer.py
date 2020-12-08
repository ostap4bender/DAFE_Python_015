import socket
import threading

from app.config import SERVER_HOST, SERVER_PORT, MESSAGE_LENGTH_LIMIT, WELCOME_MESSAGE
from app.helpers import get_input_data, get_output_data


class Client:
    server_address = (SERVER_HOST, SERVER_PORT)

    def __init__(self, login=None, token=None):
        self.login = login
        self.token = token

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            receiver = threading.Thread(target=self.receive_messages, args=(s,))
            receiver.start()
            self.send_messages(s)

    def receive_messages(self, s):
        while True:
            data = s.recv(1024)
            data = get_input_data(data)
            for message in data:
                self.process_received_message(message)

    def process_received_message(self, data):
        room, postfix, current = '', '', False
        author, message = data['author'], data['message']
        if data['event'] == 'register_user':
            self.token = data.get('token')
        elif data['event'] == 'auth_user':
            self.token = data.get('token')
        elif data['event'] == 'message_history':
            room, current = data['room'], data.get('current', False)
        elif data['event'] == 'input_message':
            room, current = data['room'], data['current']

        room = f'[{room}]' if room else ''
        postfix = '(current)' if current else ''
        print(f'{room}{postfix} {author}: {message}')

    def send_messages(self, s):
        while True:
            try:
                message = input('Type message or command. For a list of commands type /help\n')
            except EOFError:
                continue
            ok, result = self.process_command(message) if '/' in message else self.get_message_dict(message)
            if not ok:
                print(result)
                continue

            result['token'] = self.token
            data_to_send = get_output_data(result)
            s.sendto(data_to_send, self.server_address)

    def process_command(self, text):
        command, *command_params = text.split()

        if command == '/create_profile':
            if len(command_params) != 2:
                return False, '/create_profile requires exactly 2 parameters: login and password'
            else:
                login, password = command_params
                self.login = login
                return True, {'command': command, 'login': login, 'password': password}

        if command == '/auth':
            if len(command_params) != 2:
                return False, '/auth requires exactly 2 parameters: login and password'
            else:
                login, password = command_params
                self.login = login
                return True, {'command': command, 'login': login, 'password': password}

        if command == '/create_room':
            if len(command_params) != 2:
                return False, '/create_room requires exactly 2 parameters: room title, nickname for room'
            else:
                room_title, nickname_for_room = command_params
                return True, {'command': command, 'room_title': room_title, 'nickname_for_room': nickname_for_room}

        if command == '/subscribe':
            if len(command_params) != 2:
                return False, '/subscribe requires exactly 2 parameter: room title, nickname for room'
            else:
                room_title, nickname_for_room = command_params
                return True, {'command': command, 'room_title': room_title, 'nickname_for_room': nickname_for_room}

        if command == '/join':
            if len(command_params) != 1:
                return False, '/join requires exactly 1 parameter: room title'
            else:
                room_title, = command_params
                return True, {'command': command, 'room_title': room_title}

        if command == '/rooms':
            available_parameters = ['--my', '--current']
            if len(command_params) > 1:
                return False, '/rooms accepts 1 optional parameter: --my, --current'

            if len(command_params) == 1:
                which_rooms, = command_params
                if which_rooms not in available_parameters:
                    return False, '/rooms accepts 1 of: --my, --current'
                return True, {'command': command, 'which_rooms': which_rooms}
            else:
                return True, {'command': command}

        if command == '/quit':
            if command_params:
                return False, '/quit accepts no additional parameters'
            return True, {'command': command}

        if command == '/logout':
            if command_params:
                return False, '/logout accepts no additional parameters'
            self.token = None
            return True, {'command': command}

        if command == '/shutdown':
            if command_params:
                return False, '/shutdown accepts no additional parameters'
            return True, {'command': command}

        if command == '/poweron':
            if command_params:
                return False, '/poweron accepts no additional parameters'
            return True, {'command': command}

        if command == '/help':
            if command_params:
                return False, '/help accepts no additional parameters'
            return True, {'command': command}

        if len(text) > MESSAGE_LENGTH_LIMIT:
            return False, 'too long command'

        # try unknown command
        return True, {'command': command}

    def get_message_dict(self, text):
        message_dict = {
            'token': self.token,
            'message': text,
        }
        return True, message_dict


def run_client():
    print(WELCOME_MESSAGE)
    client = Client()
    client.run()
