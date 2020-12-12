'''

*Part of Chat for Client*
Во время пользования необходимо параллельно запустить файл server.py
Для изменения комнаты в чаты введите - change
Для выхода из чата введите - quit

'''

import socket
import threading
import time

class Client:
    def __init__(self):
        self.off = False
        self.in_chat = False
        self.working = True
        self.connect = False

        self.initClient()

    def takeData(self, name, sock):
        while not self.off:
            try:
                while True:
                    data, address = sock.recvfrom(1024)
                    print(data.decode("utf-8"))
                    time.sleep(0.2)
            except:
                pass

    def choseRoom(self, sock, server):
        while not self.connect:
            try:
                # создание новой комнаты под номером введённым пользователем

                port = input("Enter number of room: ")
                if port == "quit":
                    sock.close()
                    self.working = False
                    break

                sock.sendto(port.encode("utf-8"), server)
                port = int(port)
                time.sleep(0.1)

                data, address = sock.recvfrom(1024)
                if data.decode("utf-8") != "New room added":
                    print("Enter different room")
                    continue
                print(data.decode("utf-8"))

                # выбор пользователем имени комнаты

                name = input("Enter name of room: ")
                sock.sendto(name.encode("utf-8"), server)
                time.sleep(0.1)

                data, address = sock.recvfrom(1024)
                print(data.decode("utf-8"))
                if data.decode("utf-8") == "Ready to use":
                    self.connect = True
                    return port, name

            except:
                print("Warning!")

    def getMsg(self, port, host, name):
        client = (host, 9090 + port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.bind((host, 0))
        client_socket.setblocking(0)

        thread = threading.Thread(target=self.takeData, args=("RecvThread", client_socket))
        thread.start()

        while not self.off:
            if not self.in_chat:
                client_socket.sendto(("{} in chat ".format(name)).encode("utf-8"), client)
                self.in_chat = True
            else:
                try:
                    message = input()

                    if message == "change":
                        client_socket.sendto(("{} change room ".format(name)).encode("utf-8"), client)
                        self.connect = False
                        self.off = True

                    if message == "quit":
                        client_socket.sendto(("{} quit chat ".format(name)).encode("utf-8"), client)
                        self.off = True
                        self.working = False

                    if message != "":
                        client_socket.sendto(("{0} : {1}".format(name, message)).encode("utf-8"), client)

                    time.sleep(0.2)

                except:
                    client_socket.sendto(("{} out of chat ".format(name)).encode("utf-8"), client)
                    self.off = True
        thread.join()

    def startMsg(self, sock, server, host):
        while self.working:
            self.off = False
            self.in_chat = False

            port, name = self.choseRoom(sock, server)

            self.getMsg(port, host, name)

    def initClient(self):
        host = socket.gethostbyname(socket.gethostname())
        port = 0
        server = (host, 9089)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        sock.setblocking(0)

        self.startMsg(sock, server, host)

        sock.close()

if __name__ == '__main__':
    Client()


