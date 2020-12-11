import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3000

KEYWORD_DICONNECT = "00934283979723"
KEYWORD_CREATE = "0000983275890"
KEYWORD_SWITCH = "3275927034523"
KEYWORD_SUB = "0094723443045"


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]
clients = {}

default_history = ['server> server started']
rooms = {"default": {"sockets":[], "history": default_history, "names":[]}}

optional_commands = ["\create", "\sub", "\exit", "\switch"]  #\see - to show user existing rooms  (will be added)


def wrap_send_msg(message):
    msg_header = f"{len(message):< {HEADER_LENGTH}}".encode("utf-8")
    return msg_header + message.encode("utf-8")

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        
        if not len(message_header):
            return  False
        
        message_length = int(message_header.decode("utf-8").strip())
        return { "header": message_header, "data": client_socket.recv(message_length) }
        
        
    except:
        return False
    
    
def create_room(new_name, client_socket, rooms):
    try:
        
        if not new_name:
            fault_msg = wrap_send_msg("Can't create the room.")
            client_socket.send(bytes(fault_msg))
            #user = receive_message(client_socket)
            #continue
            return False
        
        uniq_name = True
        for rm in rooms:
            if rm == new_name:
                uniq_name = False
                break
            
        if not uniq_name:
            fault_msg = wrap_send_msg(f"The room {new_name} already exists.")
            client_socket.send(bytes(fault_msg))
            #user = receive_message(client_socket)
            #continue
            return False
    
        rooms[new_name] = {"sockets":[client_socket], "history": [], "names":[username]}

        print(f"room {new_name} created.")
        return new_name
    
    except:
        return False
    
    
def sub_room(msg_room, client_socket, rooms):
    try:
        
        if not msg_room or not msg_room in rooms:
            fault_msg = wrap_send_msg("Can't sub to the room.")
            client_socket.send(bytes(fault_msg))
            #user = receive_message(client_socket)
            #continue
            return False
        
        if client_socket in rooms[msg_room]["sockets"]:
            fault_msg = wrap_send_msg(f"Already subscripted to the [{msg_room}].")
            client_socket.send(bytes(fault_msg))
            return False
    
        rooms[msg_room]["sockets"].append(client_socket) #{"sockets":[server_socket, client_socket], "history": [], "names":[username]}

        print(f"sub to {msg_room}.")
        return msg_room
    
    except:
        return False
    

def remove_client(del_socket, rooms, clients):
    username = ""
    if del_socket in clients:
        username = clients[notified_socket][0]['data'].decode("utf-8")
        del clients[notified_socket]
        
    for room in rooms:
        if del_socket in rooms[room]["sockets"]:
            if room != "default":
                try:
                    rooms[room]["names"].remove(username)
                except:
                    pass
            rooms[room]["sockets"].remove(del_socket)
        
    sockets_list.remove(notified_socket)
    
    
def get_command(msg_data):
    
    msg_cmd = ""
    for i in range(len(msg_data)):
        if msg_data[i] == ' ':
            break
        msg_cmd += msg_data[i]
    
    msg_room = ""
    if len(msg_cmd) < len(msg_data) + 1:
        msg_room = msg_data[len(msg_cmd) + 1:]
        
    return (msg_cmd, msg_room)



    
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
        
            
            user = receive_message(client_socket)
            
            #print("hi here", user)
            
            if user == False:
                continue
            
            sockets_list.append(client_socket)
            clients[client_socket] = [user, {"active":"default", "subs":[]}]
            rooms["default"]["sockets"].append(client_socket)
            rooms["default"]["names"].append(user['data'].decode('utf-8'))
            
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username {user['data'].decode('utf-8')}")
            
            
            #user = receive_message(client_socket)
                               
        else:
            message = receive_message(notified_socket)
            
            if message is False:
                print(f"Closed connection from {clients[notified_socket][0]['data'].decode('utf-8')}")
                remove_client(notified_socket, rooms, clients)
                continue
            
            user = clients[notified_socket]
            username = user[0]["data"].decode("utf-8")
            
            #check if its a command:
            msg_data = message['data'].decode('utf-8')
            
            msg_cmd, msg_room = get_command(msg_data)
            
            if msg_cmd in optional_commands:
                print(f"command {msg_cmd} from user {username}, targeted room [{msg_room}]")
                cmd = msg_cmd
                if cmd == "\exit":
                    #removing notified_socket from everything
                    notified_socket.send(bytes(wrap_send_msg(KEYWORD_DICONNECT)))
                    remove_client(notified_socket, rooms, clients)
                    print(f"Closed connection from {username}")
                elif cmd == "\switch":
                    #switching the room to wich user will write
                    if not msg_room or msg_room == "default":
                        notified_socket.send(bytes(wrap_send_msg("server>")))
                        notified_socket.send(bytes(wrap_send_msg("Cant switch to room with no name and to default room.")))          
                        continue
                    
                    if msg_room in rooms:
                        if username in rooms[msg_room]["names"]:
                            notified_socket.send(bytes(wrap_send_msg("server>")))
                            notified_socket.send(bytes(wrap_send_msg(f"User with name {username} is already in the room.")))
                            continue
                        
                        prev_room = clients[notified_socket][1]["active"]
                        #debug:
                        print(f"{username} leaving room [{prev_room}]")
                        print(f"subs of user {username}: {user[1]['subs']}")
                        if not (prev_room in user[1]["subs"]):
                            rooms[prev_room]["sockets"].remove(notified_socket)
                            rooms[prev_room]["names"].remove(username)
                            print("removing suc.")
                        
                        clients[notified_socket][1]['active'] = msg_room
                        print(f"User active room now is: ", clients[notified_socket][1]['active'])
                        notified_socket.send(bytes(wrap_send_msg(KEYWORD_SWITCH + msg_room)))
                        if not (notified_socket in rooms[msg_room]["sockets"]):
                            rooms[msg_room]["sockets"].append(notified_socket)
                        rooms[msg_room]["names"].append(username)
                            
                    else:
                        notified_socket.send(bytes(wrap_send_msg("server>")))
                        notified_socket.send(bytes(wrap_send_msg("No such room.")))
                    
                elif cmd == "\create":
                    if not msg_room:
                        notified_socket.send(bytes(wrap_send_msg("Cant create the room with no name.")))
                        
                    rm_name = create_room(msg_room, notified_socket, rooms)
                    if rm_name:
                        print(f"[{rm_name}] room created succesfully by {username}")
                        notified_socket.send(bytes(wrap_send_msg(KEYWORD_CREATE + rm_name)))
                        prev_room = clients[notified_socket][1]["active"]
                        if not (prev_room in user[1]["subs"]):
                            rooms[prev_room]["sockets"].remove(notified_socket)
                            rooms[prev_room]["names"].remove(username)
                            
                        clients[notified_socket][1]["active"] = rm_name
                    else:
                        print("creation of room failed")
                        
                elif cmd == "\sub":
                    #adding user to the recivers of the room (user will receive msgs from that room)
                    if not msg_room:
                        notified_socket.send(bytes(wrap_send_msg("Cant sub to room with no name.")))
                        
                    rm_name = sub_room(msg_room, notified_socket, rooms)
                    if rm_name:
                        print(f"{username} succesfully sub to [{rm_name}]")
                        user[1]["subs"].append(rm_name)
                        #send history
                        HISTORY = f"Sub to [{rm_name}] confirmed.\nHistory of [{rm_name}]:\n"
                        for hmsg in rooms[rm_name]["history"]:
                            HISTORY += (hmsg + '\n')
                        HISTORY += "--- that's all.\n"
                        notified_socket.send(bytes(wrap_send_msg(KEYWORD_SUB + HISTORY)))
                    else:
                        print("sub to room failed")
                        notified_socket.send(bytes(wrap_send_msg(f"sub to room [{msg_room}] failed.")))
                        
                continue
            
            print(f"Received message from [{user[1]['active']}]{user[0]['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            

            #sends messages to clients in his current room
            active_room = user[1]["active"]
            #for client_socket in clients: 
            for client_socket in rooms[active_room]["sockets"]: 
                if client_socket != notified_socket:   #and clients[client_socket][1]["active"] == active_room:
                    usrnm = user[0]['data'].decode("utf-8")
                    user_info = wrap_send_msg(f"[{active_room}]" + usrnm)
                    
                    new_msg_txt = f"[{active_room}]{usrnm}> {message['data'].decode('utf-8')}"
                    new_message = user_info + message['header'] + message['data'] #in bytes
                    #new_message = user[0]["header"] + user[0]["data"] + message["header"] + message["data"]
                    client_socket.send(bytes(new_message))
                    rooms[active_room]["history"].append(new_msg_txt)
                    
                    #print(f"History of room [{active_room}] updated.")
                    #print(rooms[active_room]["history"])
                
                    
                    
    for notified_socket in exception_sockets:
        remove_client(notified_socket, rooms)
                