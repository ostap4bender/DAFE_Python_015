from Socket import Socket
import threading


class Channel:
    def __init__(self, name):
        self.story = []
        self.subscribers = []
        self.name = name


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()

        print('Server is listening')

        self.users = []
        self.channels = []

    def set_up(self):
        self.bind(('127.0.0.1', 1234))
        self.listen()

        create_channel = threading.Thread(target=self.create_channel)
        create_channel.start()

        self.accept_sockets()

    def create_base_channel(self):
        channel1 = Channel('Channel1')
        channel2 = Channel('Channel2')
        channel3 = Channel('Channel3')
        self.channels.append(channel1)
        self.channels.append(channel2)
        self.channels.append(channel3)

    def create_channel(self):
        self.create_base_channel()
        while True:
            _input = input()
            if _input[:8] == 'create "' and _input[-1] == '"':
                name_channel = _input[8:-1]
                if len(name_channel) > 30 or len(name_channel) < 4:
                    print('Error: chars > 30 or chars < 4 ')
                    continue
                if self.find_channel(name_channel):
                    print('Error: such a channel already exists')
                    continue

                new_channel = Channel(name_channel)
                self.channels.append(new_channel)
                print(f'Channel with name <{name_channel}> was created')
            else:
                print("Error: wrong input")

    def send_data(self, nickname, channel, data):
        i = self.find_channel_in_list(channel.decode('utf-8'))
        self.channels[i].story.append([nickname, data])
        if len(self.channels[i].story) > 128:
            del self.channels[i].story[0]

        for user in self.users:

            user_socket = user[0]
            user_channel = user[2]

            if user_channel == channel:
                nickname = nickname.decode('utf-8')
                nickname = nickname.encode('utf-8')
                user_socket.send(nickname)
                user_socket.send(data)

    def listen_socket(self, listened_socket=None):
        nickname = self.users[-1][1]
        channel = self.users[-1][2]
        while True:
            data = listened_socket.recv(254)

            if data.decode('utf-8') == '/quit':
                i = self.find_user_in_list(nickname)

                self.users[i][0].send('something'.encode('utf-8'))
                self.users[i][0].send(data)

                channel = self.get_user_channel(self.users[i][0], self.users[i][3], self.users[i][1])
                self.users[i][2] = channel

            else:
                print(f'<{nickname.decode("utf-8")}> sent "{data.decode("utf-8")}" on {channel}')
                self.send_data(nickname, channel, data)

    def find_user_in_list(self, nickname):
        for i in range(len(self.users)):
            if self.users[i][1] == nickname:
                return i

    def find_channel_in_list(self, channel_name):
        for i in range(len(self.channels)):
            if self.channels[i].name == channel_name:
                return i

    def find_name(self, name):
        for user in self.users:
            if user[1].decode('utf-8') == name:
                return True
        return False

    def find_channel(self, channel_name):
        for channel in self.channels:
            if channel.name == channel_name:
                return True
        return False

    def get_user_nickname(self, user_socket):
        user_nickname = None
        while True:
            user_nickname = user_socket.recv(254)
            if not (self.find_name(user_nickname.decode('utf-8'))):
                user_socket.send('OK'.encode('utf-8'))
                break
            user_socket.send('wrong nickname'.encode('utf-8'))
        return user_nickname


    def get_user_channel(self, user_socket, list_of_channels, kkuser_nickname):
        Flag = False
        kkchannel = ''
        while True:
            user_channel = user_socket.recv(254)
            if self.find_channel(user_channel.decode('utf-8')):
                if user_channel.decode('utf-8') in list_of_channels:
                    user_socket.send('OK'.encode('utf-8'))
                else:
                    user_socket.send(f'Do you want to subscribe on '
                                     f'{user_channel.decode("utf-8")}? (Yes or No)'.encode('utf-8'))

                    answer = user_socket.recv(254)
                    if answer.decode('utf-8') == 'Yes':
                        list_of_channels.append(user_channel.decode('utf-8'))
                        user_socket.send('OK'.encode('utf-8'))
                        kkchannel = user_channel
                        Flag = True
                    else:
                        user_socket.send('  '.encode('utf-8'))
                        continue
                break
            user_socket.send('wrong channel'.encode('utf-8'))
        temp = user_socket.recv(254)
        if Flag:
            Flag = False
            kkuser_nickname.decode('utf-8')
            kkuser_nickname = kkuser_nickname.decode('utf-8')
            kkuser_nickname += ' join the room'
            self.send_data('room'.encode('utf-8'), kkchannel, kkuser_nickname.encode('utf-8'))

        self.give_story_to_user(user_socket, user_channel)

        return user_channel

    def give_story_to_user(self, user_socket, user_channel):
        i = self.find_channel_in_list(user_channel.decode('utf-8'))
        line = ' |'
        for vec in self.channels[i].story:
            line += vec[0].decode('utf-8') + ': ' + vec[1].decode('utf-8') + '|'
        if line != ' |':
            user_socket.send(line.encode('utf-8'))
        else:
            user_socket.send(' '.encode('utf-8'))

    def accept_sockets(self):

        while True:
            starter_list_channels = ['Channel1', 'Channel2', 'Channel3']
            user_socket, address = self.accept()
            user_nickname = self.get_user_nickname(user_socket)

            self.users.append([user_socket, user_nickname, '0'.encode('utf-8'), starter_list_channels])

            user_channel = self.get_user_channel(self.users[-1][0], self.users[-1][3], self.users[-1][1])
            self.users[-1][2] = user_channel

            print(f'User {user_nickname.decode("utf-8")} connected to {user_channel.decode("utf-8")}!')

            listen_accepted_user = threading.Thread(target=self.listen_socket, args=(user_socket,))
            listen_accepted_user.start()


if __name__ == '__main__':
    server = Server()
    server.set_up()


#                  py C:\Users\user\Desktop\Messenger\client.py
