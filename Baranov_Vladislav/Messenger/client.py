from Socket import Socket
from threading import Thread
import os


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.nickname = None
        self.status = 0
        self.mychannels = ['Channel1', 'Channel2', 'Channel3']

    def set_up(self):
        self.connect(('127.0.0.1', 1234))

        self.check_nickname()

        self.check_channel()

        listen_thread = Thread(target=self.listen_server)
        listen_thread.start()

        send_thread = Thread(target=self.send_data, args=(None, None, None,))
        send_thread.start()

    def listen_server(self):
        while True:

            input_nickname = self.recv(254)
            data = self.recv(254)

            if data.decode('utf-8') == '/quit':
                print('\r', end='')
                os.system("cls")

                self.check_channel()

                self.status = 0

            elif input_nickname.decode('utf-8') != self.nickname:
                print('\r', end='')
                print(f'{input_nickname.decode("utf-8")}: {data.decode("utf-8")} \n{self.nickname}: ', end='')

    def send_data(self, nickname, channel, data):
        while True:
            if self.status == 0:
                _input = input(self.nickname + ': ')
                self.send(_input.encode('utf-8'))
                if _input == '/quit':
                    self.status = 1

    # def get_story(self):
    #     self.send()

    def check_nickname(self):
        while True:
            self.nickname = input('Enter your nickname: ')
            if len(self.nickname) > 3:
                self.send(self.nickname.encode('utf-8'))
                status = self.recv(254)
                if status.decode('utf-8') == 'OK':
                    break
                print('Error: such name already exists')
            else:
                print('Error: length of name < 3')

    def print_list_channels(self):
        print('Your Channels:')
        for channel in self.mychannels:
            print('  ' + channel)
        print('')

    def check_channel(self):

        self.print_list_channels()
        while True:

            _input = input('Enter channel: ')
            if len(_input) == 0:
                continue

            self.send(_input.encode('utf-8'))
            status = self.recv(254)

            if status.decode('utf-8') == 'wrong channel':
                print('Error: nonexistent channel')

            elif status.decode('utf-8') == 'OK':
                pass

            else:
                print(status.decode('utf-8'))
                self.send(input('Answer: ').encode('utf-8'))
                status = self.recv(254)
                if status.decode('utf-8') == 'OK':
                    self.mychannels.append(_input)

            if status.decode('utf-8') == 'OK':
                self.send('OK'.encode('utf-8'))

                os.system("cls")

                message = self.recv(330000).decode('utf-8').split('|')

                for line in message:
                    print(line)
                break


if __name__ == '__main__':
    client = Client()
    client.set_up()
