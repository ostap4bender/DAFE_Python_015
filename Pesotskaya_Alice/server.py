import socket, time, threading

HISTORY_LEN = 128
port = 0
rooms = []


def room(name, port):
    host = socket.gethostbyname(socket.gethostname())

    clients = []
    history = []

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    quit = False
    print("[Server Started]", (host, port))

    while not quit:
        try:
            show_message = True
            data, addr = s.recvfrom(255)

            if addr not in clients:
                clients.append(addr)
                for el in history:
                    s.sendto(el.encode("utf-8"), addr)

            splitted = data.decode("utf-8").split(":")
            if len(splitted) == 3:
                if splitted[2] == "q" or splitted[2] == "s": 
                    clients.remove(addr)
                    # print(clients)
                    show_message = False


            itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
            if show_message:
                msg = "[" + addr[0] + "]=[" + str(addr[1]) + "]=[" + itsatime + "]/ " + data.decode("utf-8")
                print(msg)
                if len(history) > HISTORY_LEN:
                    history.pop(0)
                history.append(data.decode("utf-8"))


            for client in clients:
                if addr != client:
                    # print(client)
                    s.sendto(data, client)

        except:
            print("\n[ Server stopped]")
            quit = True

    s.close()


def main(*args):
    print("Server started\n")

    rooms = []
    rooms_names = {}
    host = socket.gethostbyname(socket.gethostname())

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = (host, 9089)
    s.bind(server)
    while True:
        data, addr = s.recvfrom(255)
        try:
            port = 9090 + int(data.decode("utf-8"))
            if port >= 2**16 or port <9090:
                raise OverflowError

            if not port in rooms:
                print("Created room")
                rm = threading.Thread(target=room, args=("tryz", port))
                rm.start()
                rooms.append(port)
                rooms_names[port] = []

            s.sendto(("Room exist").encode("utf-8"), addr)

            data, addr = s.recvfrom(255)
            if data.decode() in rooms_names[port]:
                s.sendto(("Name already in use").encode("utf-8"), addr)
            else:
                rooms_names[port].append(data.decode())
                s.sendto(("Connected").encode("utf-8"), addr)

        except:
            warning = "something went wrong"
            s.sendto((warning.encode("utf-8")), addr)


if __name__ == '__main__':
    main()
