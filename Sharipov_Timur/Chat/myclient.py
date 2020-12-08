import socket
import threading
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

ALLOWED = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-"

COMMANDS = {
    '/create [roomname]': 'create room',
    '/rooms [key or none]': 'list of rooms, flags: -all, -my',
    '/sub [roomname] as [nickname]': 'subscribe the room',
    '/join [roomname]': 'join to the room',
    '/quit': 'quit from current room',
    '/clear' : 'clear console'
} 


def print_intro():
    print("Welcome to chat!")
    print("Available commands:")
    for cmd in COMMANDS.keys():
        print(" > {} - {}".format(cmd, COMMANDS[cmd]))
    print()


def main(serv, cl):
    shutdown = False

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(cl)

    print_intro()

    def receiving(s):
        while not shutdown:
            try:
                data, addr = s.recvfrom(254)
                data = data.decode("utf-8")
                if data == "/clear":
                    os.system("cls")
                else:
                    print(data)
            except RuntimeError:
                break

    rt = threading.Thread(target=receiving, args=(client,))
    rt.start()

    # Initialize message
    client.sendto("/".encode("utf-8"), server)

    while not shutdown:
        try:
            message = input().strip()

            if message != "":
                client.sendto(f"{message}".encode("utf-8"), server)

        except BaseException:
            client.sendto(f"/exit".encode("utf-8"), server)
            shutdown = True

    # rt.join()
    client.close()


if __name__ == "__main__":
    server = (SERVER_HOST, SERVER_PORT)
    client = (SERVER_HOST, 0)

    main(server, client)