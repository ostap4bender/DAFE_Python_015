import socket
import threading
import config


def print_intro():
    print("Welcome to chat!")
    print("Available commands:")
    for cmd in config.COMMANDS.keys():
        print(" > {} - {}".format(cmd, config.COMMANDS[cmd]))
    print()


def main(serv, cl):
    shutdown = False

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(cl)
    # sock.setblocking(False)

    print_intro()

    def receiving(s):
        while not shutdown:
            try:
                while True:
                    data, addr = s.recvfrom(1024)

                    print("{}".format(data.decode("utf-8")))
            except RuntimeError:
                pass

    rt = threading.Thread(target=receiving, args=(sock,))
    rt.start()

    # Initialize message
    sock.sendto("/".encode("utf-8"), server)

    while not shutdown:
        try:
            message = input().strip()

            if message != "":
                sock.sendto(f"{message}".encode("utf-8"), server)

        except BaseException:
            sock.sendto(f"/exit".encode("utf-8"), server)
            shutdown = True

    rt.join()
    sock.close()


if __name__ == "__main__":
    server = (config.SERVER_HOST, config.SERVER_PORT)
    client = (config.SERVER_HOST, 0)

    main(server, client)
