import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3000

KEYWORD_DICONNECT = "00934283979723"
KEYWORD_CREATE = "0000983275890"
KEYWORD_SWITCH = "3275927034523"


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]
clients = {}

default_history = ['server> 1', 'server> 2','server> 3','server> server started']

rooms = {"default": {"sockets":[server_socket], "history": default_history, "names":[]}}
users_online = []


optional_commands = ["\create", "\sub", "\exit", "\swich"]


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
    
        rooms[new_name] = {"sockets":[server_socket, client_socket], "history": [], "names":[username]}

        print(f"room {new_name} created.")
        return new_name
    
    except:
        return False
    
    
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
            
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username {user['data'].decode('utf-8')}")
            
            
            #user = receive_message(client_socket)
                               
        else:
            message = receive_message(notified_socket)
            
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            user = clients[notified_socket]
            username = user[0]["data"].decode("utf-8")
            
            #check if its a command:
            msg_data = message['data'].decode('utf-8')
            
            
                
            msg_cmd = ""
            for i in range(len(msg_data)):
                if msg_data[i] == ' ':
                    break
                msg_cmd += msg_data[i]
            
            msg_room = ""
            if len(msg_cmd) < len(msg_data) + 1:
                msg_room = msg_data[len(msg_cmd) + 1:]
            
            if msg_cmd in optional_commands:
                print(f"command {msg_cmd} from user {username}, targeted room {msg_room}")
                cmd = msg_cmd
                if cmd == "\exit":
                    #removing notified socket from everything
                    notified_socket.send(bytes(wrap_send_msg(KEYWORD_DICONNECT)))
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]                    
                    #from rooms also
                    print(f"Closed connection from {username}")
                elif cmd == "\switch":
                    #switching the room to wich user will write
                    if msg_room in rooms:
                        clients[notified_socket][1]["active"] = rm_name
                        notified_socket.send(bytes(wrap_send_msg(KEYWORD_SWITCH + msg_room)))
                    else:
                        notified_socket.send(bytes(wrap_send_msg("No such room.")))
                    
                elif cmd == "\create":
                    if not msg_room:
                        notified_socket.send(bytes(wrap_send_msg("Cant create the room with no name.")))
                    rm_name = create_room(msg_room, notified_socket, rooms)
                    if rm_name:
                        print(f"[{rm_name}] room created succesfully by {username}")
                        notified_socket.send(bytes(wrap_send_msg(KEYWORD_CREATE + rm_name)))
                        clients[notified_socket][1]["active"] = rm_name
                    else:
                        print("creation of room failed")
                elif cmd == "\sub":
                    #adding user to the room
                    pass
                continue
            
            print(f"Received message from {user[0]['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            
            
            #Here wewant to send it only to the user with common rooms
            #Or only for one room
            #Only for users from curent room of user
            
            #what we send:
            
            #text = user['header'] + user['data'] + message['header'] + message['data']
            
            #for clients in his current room
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user[0]['header'] + user[0]['data'] + message['header'] + message['data'])
                    
                    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]