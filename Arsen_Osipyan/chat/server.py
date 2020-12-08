import socket
import time
import config
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


clients = []
rooms = []


class Room:
    def __init__(self, name):
        self.subs = dict()  # Client: name_in_this_room
        self.name = name
        self.history = []  # consists of (addr, name, message)

    def publish(self, serv, addr, msg):
        self.history.append((addr, self.subs[get_client(addr)], msg))
        for cl in self.subs.keys():
            if cl.addr != addr and cl.cur_room == self.name:
                serv.sendto("[{}] {}".format(self.subs[get_client(addr)], msg).encode('utf-8'), cl.addr)

    def send_history(self, serv, addr):
        if len(self.history) <= config.ROOM_STORY_LENGTH:
            for msg in self.history:
                serv.sendto("[{}] {}".format(msg[1], msg[2]).encode('utf-8'), addr)
        else:
            for msg in self.history[:-config.ROOM_STORY_LENGTH-1:-1]:
                serv.sendto("[{}] {}".format(msg[1], msg[2]).encode('utf-8'), addr)


class Client:
    def __init__(self, addr):
        self.addr = addr
        self.rooms = []
        self.cur_room = ''


def get_client(addr):
    for c in clients:
        if c.addr == addr:
            return c
    return False


def get_room(name):
    for r in rooms:
        if r.name == name:
            return r
    return False


def generate_msg(msg):
    return "[Server] {}".format(msg).encode("utf-8")


def handle_command(serv, msg, addr):
    params = list(msg.strip().split())
    cmd = params[0]
    params = params[1:]

    if cmd == '/' and len(params) == 0:
        if not get_client(addr):
            clients.append(Client(addr))
            print("[Server] New user {}:{}".format(addr[0], addr[1]))
        else:
            serv.sendto(generate_msg("Incorrect command"), addr)

    elif cmd == '/create' and len(params) == 1:
        if not get_room(params[0]):
            rooms.append(Room(params[0]))
            print("[Server] New room {} created by {}:{}".format(params[0], addr[0], addr[1]))
        else:
            serv.sendto(generate_msg("Room name must be unique"), addr)

    elif cmd == '/ls' and len(params) == 1:
        if params[0] == '-all':
            if not rooms:
                serv.sendto(generate_msg("No rooms"), addr)
            for r in rooms:
                serv.sendto(generate_msg("- {}".format(r.name)), addr)
        elif params[0] == '-my':
            if not get_client(addr).rooms:
                serv.sendto(generate_msg("You haven't subscribed for any rooms"), addr)
            else:
                for r_name in get_client(addr).rooms:
                    serv.sendto(generate_msg("- {}".format(r_name)), addr)
        else:
            serv.sendto(generate_msg("Incorrect parameter"), addr)

    elif cmd == '/sub' and len(params) == 2:
        room = get_room(params[0])
        if room:
            for cl in room.subs.keys():
                if cl.addr == addr:
                    serv.sendto(generate_msg("You are in this room"), addr)
                    break
            else:
                for name in room.subs.values():
                    if name == params[1]:
                        serv.sendto(generate_msg("Try another name"), addr)
                        break
                for i in range(len(rooms)):
                    if rooms[i].name == params[0]:
                        rooms[i].subs[get_client(addr)] = params[1]
                        break
                for i in range(len(clients)):
                    if clients[i].addr == addr:
                        clients[i].rooms.append(params[0])
                        break
                print("[Server] User {}:{} subscribed {} with name {}".format(addr[0], addr[1], params[0], params[1]))
        else:
            serv.sendto(generate_msg("Room does not exist"), addr)

    elif cmd == '/join' and len(params) == 1:
        room = get_room(params[0])
        if room:
            for cl in room.subs.keys():
                if cl.addr == addr:
                    for i in range(len(clients)):
                        if clients[i].addr == addr:
                            clients[i].cur_room = params[0]
                            break
                    for i in range(len(rooms)):
                        if rooms[i].name == params[0]:
                            rooms[i].send_history(serv, addr)
                            break
                    break
            else:
                serv.sendto(generate_msg("You didn't subscribe this room"), addr)
        else:
            serv.sendto(generate_msg("Room does not exist"), addr)

    elif cmd == '/quit' and len(params) == 0:
        cur_room = get_client(addr).cur_room
        if cur_room:
            for i in range(len(clients)):
                if clients[i].addr == addr:
                    clients[i].cur_room = ''
                    break
        else:
            serv.sendto(generate_msg("You are not in room"), addr)

    elif cmd == '/exit' and len(params) == 0:
        if get_client(addr):
            for r_name in get_client(addr).rooms:
                for i in range(len(rooms)):
                    if rooms[i].name == r_name:
                        del rooms[i].subs[get_client(addr)]
                        break
            for i in range(len(clients)):
                if clients[i].addr == addr:
                    clients.remove(clients[i])
                    break
            print("[Server] User {}:{} left chat".format(addr[0], addr[1]))

    else:
        serv.sendto(generate_msg("Incorrect command or number of params"), addr)


def handle_message(serv, msg, addr):
    cur_room = get_client(addr).cur_room

    if cur_room:
        for i in range(len(rooms)):
            if rooms[i].name == cur_room:
                rooms[i].publish(serv, addr, msg)
    else:
        serv.sendto(generate_msg("You are not in room"), addr)


def main(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    print("[Server] Server started at {}:{}".format(host, port))

    while True:
        try:
            data, addr = server.recvfrom(1024)
            data = data.decode('utf-8')

            if data[0] == '/':  # handling commands
                handle_command(server, data, addr)
            else:               # handling common messages
                handle_message(server, data, addr)

            time.sleep(0.5)

        except BaseException:
            print("[Server] Server stopped")
            break

    server.close()


if __name__ == '__main__':
    main(config.SERVER_HOST, config.SERVER_PORT)
