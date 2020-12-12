'''

*Server of Chat*
Во время пользования необходимо параллельно запустить файл client.py

'''

import socket
import threading

messages_count = 128

class Server:
    def __init__(self):
        self.initServer()

    def newThread(self, name, port):
        host = socket.gethostbyname(socket.gethostname())
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))

        clients = []
        messages = []

        quit = False
        print("Number of server: ", (host, port))

        while not quit:
            try:
                data, address = sock.recvfrom(1024)

                if address not in clients:
                    clients.append(address)
                    for msg in messages:
                        sock.sendto(msg.encode("utf-8"), address)

                show = True
                last_message = data.decode("utf-8").split(' ')
                if len(last_message) == 3:
                    if last_message[2] == "change" or last_message[2] == "quit":
                        clients.remove(address)
                        show = False
                        if last_message[2] == "quit":
                            quit = True
                            print("\nEnd of server")

                if show:
                    message = '{' + address[0] + '} ' + data.decode("utf-8")
                    print(message)
                    if len(messages) > messages_count:
                        messages.pop(0)
                    messages.append(data.decode("utf-8"))

                for client in clients:
                    if address != client:
                        sock.sendto(data, client)
            except:
                print("\nEnd of server")
                quit = True

        sock.close()

    def initServer(self):
        print("Begin of server")

        host = socket.gethostbyname(socket.gethostname())
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = (host, 9089)
        sock.bind(server)

        threads = []
        names = {}

        while True:
            data, address = sock.recvfrom(1024)
            try:
                port = 9090 + int(data.decode("utf-8"))
                if port >= 2 ** 16 or port < 9090:
                    raise OverflowError

                if port not in threads:
                    print("New room added")
                    thread = threading.Thread(target=self.newThread, args=("tryz", port))
                    thread.start()
                    threads.append(port)
                    names[port] = []

                sock.sendto("New room added".encode("utf-8"), address)

                data, address = sock.recvfrom(1024)
                if data.decode() in names[port]:
                    sock.sendto("This name is already use".encode("utf-8"), address)
                else:
                    names[port].append(data.decode())
                    sock.sendto("Ready to use".encode("utf-8"), address)

            except:
                warning = "something went wrong"
                sock.sendto((warning.encode("utf-8")), address)

if __name__ == '__main__':
    Server()

