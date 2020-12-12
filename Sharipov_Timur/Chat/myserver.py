import socket
import time
import config
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


clients = list()  #list of users
rooms = list()  #list of rooms

def get_user(addr):
    for u in clients:
        if u.addr == addr:
            return u
    return False

class User():
    def __init__(self, addr):
        self.addr = addr
        self.rooms = list()
        self.curr_room = ""

class Room():
    def __init__(self, name, serv):
        self.subs = dict()  # dict of user:name_in_this_room
        self.name = name
        self.history = list()  # list of (name_in_this_room, message)
        self.serv = serv

    def new_message(self, user, msg: str):
        name = self.subs[user]
        self.history.append((name, msg))
        if len(self.history) == config.ROOM_STORY_LENGTH + 1:
            self.history = self.history[1:]
        for us in self.subs.keys():
            if us.addr != user.addr and us.curr_room == self:
                self.serv.sendto("[{}] {}".format(name, msg).encode('utf-8'), us.addr)

    def new_joined(self, user):
        name = self.subs[user]
        self.history.append(("{} joined".format(name), ""))
        if len(self.history) == config.ROOM_STORY_LENGTH + 1:
            self.history = self.history[1:]
        for us in self.subs.keys():
            if us.addr != user.addr and us.curr_room == self:
                self.serv.sendto("[{} joined this room]".format(name).encode('utf-8'), us.addr)

    def new_leaved(self, user):
        name = self.subs[user]
        self.history.append(("{} leaved".format(name), ""))
        if len(self.history) == config.ROOM_STORY_LENGTH + 1:
            self.history = self.history[1:]
        for us in self.subs.keys():
            if us.addr != user.addr and us.curr_room == self:
                self.serv.sendto("[{} leaved this room]".format(name).encode('utf-8'), us.addr)



    def subscribe(self, user: User, name : str):
        for us in self.subs.values():
            if name == us:
                self.serv.sendto("    Sorry, this nick has been already registered".encode('utf-8'), user.addr)
                return
        self.serv.sendto("    <server>: You registered in {} as {}".format(self.name, name).encode('utf-8'), user.addr)
        self.subs[user] = name

    def print_history(self, addr):
        for i in self.history:
            if i[1] == "":
                self.serv.sendto("[{}]".format(i[0]).encode("utf-8"), addr)
            else:   
                self.serv.sendto("[{}] : {}".format(i[0], i[1]).encode("utf-8"), addr)



class Server():
    def __init__(self):
        self.host = config.SERVER_HOST
        self.port = config.SERVER_PORT
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))
        print("<server>: started on {}:{}".format(self.host, self.port))
        rooms.append(Room("HUB", self.server))
        self.main_loop()

    def main_loop(self):
        while True:
            try:
                data, addr = self.server.recvfrom(254)
                data = data.decode("utf-8")
                if data[0] == "/": 
                    self.command(data, addr)
                else:              
                    self.message(data, addr)

                time.sleep(0.1)

            except RuntimeError:
                print("<server> server stopped")
                break

        server.close()


    def help(self, addr):
        for command in config.COMMANDS.keys():
            self.server.sendto("{} : {}".format(command, config.COMMANDS[command]).encode("utf-8"), addr)

    def message(self, data, addr):

        curr_user = get_user(addr)
        if curr_user.curr_room == "":
            self.server.sendto("    <server>: Incorrect command. Use \"/\" to learn more".encode('utf-8'), addr)
            return
        else:
            curr_user.curr_room.new_message(curr_user, data)
            print("{}: {}".format(curr_user.addr[0], data))

    def command(self, data, addr):

        ip = addr[0]
        user_port = addr[1]
        params = list(data.strip().split())
        if params[0] == '/exit':
            curr_user = get_user(addr)
            if curr_user:
                for r in rooms:
                    for us in r.subs:
                        if us.addr == addr:
                            rooms.remove(us)
                            break
                for us in clients:
                    if us.addr == addr:
                        clients.remove(us)
                        break
            print("User {} exit".format(addr))
            return

        # print(params)
        curr_user = get_user(addr)
        if curr_user == False:
            print("<server>: registered {}:{}".format(ip, user_port))
            clients.append(User(addr))
            return
        if curr_user.curr_room == "":
            if params[0] == "/" and len(params) == 1:
                for cl in clients:
                    if cl.addr == addr:
                        self.help(addr)
                        return
                print("<server>: registered {}:{}".format(ip, user_port))
                clients.append(User(addr))
                return
            if params[0] == "/create":
                if len(params) == 2:
                    name = str(params[1])
                    if name[0] not in config.ALLOWED:
                        self.server.sendto("    <server>: You can't create rooms with name started with this symbol".format(name).encode('utf-8'), addr)
                        return
                    for r in rooms:
                        if r.name == name:
                            self.server.sendto("    <server>: This room is already exist".format(name).encode('utf-8'), addr)
                            return
                    rooms.append(Room(name, self.server))
                    print("<server>: room created as {} by {}:{}".format(name, ip, user_port))
                    self.server.sendto("    <server>: You created room {}".format(name).encode('utf-8'), addr)
                    return
                else:
                    self.server.sendto("    <server>: You must use this semantic: \"/create [roomname]\"".encode('utf-8'), addr)
                    return

            if params[0] == "/clear":
                if len(params) == 1:
                    self.server.sendto("/clear".encode('utf-8'), addr)
                    return
                else:
                    self.server.sendto("    <server>: You must use this semantic: \"/clear\"".encode('utf-8'), addr)
                    return



            if params[0] == "/rooms":
                if len(params) == 1 or (len(params)==2 and params[1] == "-all"):
                    self.server.sendto("Rooms avaliable:".encode("utf-8"), addr)
                    for i in rooms:
                        self.server.sendto(("   " + i.name).encode("utf-8"), addr)
                    return
                elif len(params) == 2:
                    self.server.sendto("Rooms avaliable:".encode("utf-8"), addr)
                    if params[1] == "-my":
                        for r in rooms:
                            for us in r.subs:
                                if us.addr == addr:
                                    self.server.sendto(("    " + r.name).encode("utf-8"), addr)
                        return
                    else:
                        self.server.sendto("    <server>: Unknown key. Avaliable keys: -all, -my".encode('utf-8'), addr)
                        return


                else:
                    self.server.sendto("    <server>: You must use this command itself only or with one of keys: -all, -my".encode('utf-8'), addr)
                    return

            if params[0] == "/sub":
                if len(params) == 4 and params[2] == "as":
                    for r in rooms:
                        if r.name == params[1]:
                            curr_user = get_user(addr)
                            if curr_user == False:
                                print("ERROR in /sub: no user found")
                                return
                            for us in r.subs:
                                if us.addr == addr:
                                    self.server.sendto("    <server>: You've already subscribed this room".encode('utf-8'), addr)
                                    return
                            r.subscribe(curr_user, params[3])
                            return
                    self.server.sendto("    <server>: This room does not exist".encode('utf-8'), addr)
                    return
                else:
                    self.server.sendto("    <server>: You must use this semantic: \"/sub [roomname] as [nickname]\"".encode('utf-8'), addr)
                    return
            if params[0] == "/join":
                if len(params) == 2:
                    for r in rooms:
                        if r.name == params[1]:
                            curr_user = get_user(addr)
                            flag = False
                            for us in r.subs:
                                if us.addr == addr:
                                    flag = True
                                    break
                            if not flag:
                                self.server.sendto("You didn't subscribe {} room".format(r.name).encode("utf-8"), addr)
                                return
                            if curr_user == False:
                                print("ERROR in /join")
                                return
                            curr_user.curr_room = r
                            self.server.sendto("You joined to the room {}".format(r.name).encode("utf-8"), addr)
                            print("User {} joined to the room {}".format(curr_user.addr[0], r.name))
                            r.print_history(addr)
                            r.new_joined(curr_user)
                            return
                    self.server.sendto("    <server>: This room does not exist".encode('utf-8'), addr)
                else:
                    self.server.sendto("    <server>: You must use this semantic: \"/join [roomname]\"".encode('utf-8'), addr)
                    return

            else:
                self.server.sendto("    <server>: Incorrect command. Use \"/\" to learn more".encode('utf-8'), addr)
                return
        else:
            if params[0] == "/" and len(params) == 1:
                self.server.sendto("\"/quit\" : leave current room\n\"/clear\" : clear console".encode("utf-8"), addr)
                return

            if params[0] == "/quit" and len(params) == 1:
                curr_user = get_user(addr)
                if curr_user == False:
                    self.server.sendto("    <server>: no user found".encode('utf-8'), addr)
                    return
                print("{} leaved room {}".format(curr_user.addr, curr_user.curr_room.name))
                curr_user.curr_room.new_leaved(curr_user)
                self.server.sendto("You leaved room {}".format(curr_user.curr_room.name).encode("utf-8"), addr)
                curr_user.curr_room = ""
                return
            if params[0] == "/clear":
                if len(params) == 1:
                    self.server.sendto("/clear".encode('utf-8'), addr)
                    return
                else:
                    self.server.sendto("    <server>: You must use this semantic: \"/clear\"".encode('utf-8'), addr)
                    return
            else:
                self.server.sendto("    <server>: Incorrect command. Use \"/\" to learn more".encode('utf-8'), addr)
                return


if __name__ == '__main__':
    try:
        s = Server()
    except:
        print("fall fall fall fall fall fall fall fall fall fall fall fall fall fall fall fall fall fall ")
        input()