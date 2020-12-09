import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3000


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]
clients = {}

rooms = {"default": {"sockets":[server_socket], "history": ['1', '2','3','server started', 'default room'], "names":[]}}
users_online = []

optional_comands = ["\create  -  to create a room", "\sub  to subscribe to existing room",
                    "\cancel  -  to cancel while subscr.", "\exit  -  to leave the server"]

def wrap_send_msg(message):
    msg_header = f"{len(message):< {HEADER_LENGTH}}".encode("utf-8")
    return msg_header + message.encode("utf-8")

def decode_rcvd(message):
    pass

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        
        if not len(message_header):
            return  False
        
        message_length = int(message_header.decode("utf-8").strip())
        return { "header": message_header, "data": client_socket.recv(message_length) }
        
        
    except:
        return False
    
    
def get_room_name(client_socket):
    try:
        msg = wrap_send_msg("input room name")
        
        client_socket.send(bytes(msg))
        message_header = client_socket.recv(HEADER_LENGTH)
        
        if not len(message_header):
            return  False
        
        message_length = int(message_header.decode("utf-8").strip())
        user_try = client_socket.recv(message_length)
        room_name = user_try.decode("utf-8")
        
        
        return room_name
        
    except:
        return False 
    
def connect_client(user, client_socket, server_socket, rooms):
    '''
    welcome_message = "Hi on the chat server!" #Please choose one of avalible chat-rooms:\n"
    for room in rooms:
        welcome_message += (room + '\n')
    welcome_message += "Or create your own ( to do that input \create )"
    '''
    welcome_message = "Hi on the chat server!\nOptional commands:\n"
    for cmd in optional_comands:
        welcome_message += (cmd + '\n')
    
    welcome_message = wrap_send_msg(welcome_message)
    client_socket.send(bytes(welcome_message))
    
    username = user['data'].decode('utf-8')
    user = receive_message(client_socket)
    
    result = False
    while user != False:
        user_ans = user["data"].decode("utf-8")
        if user_ans == "\create":
            
            print(f"User {username} wants to create a room")
            new_name = get_room_name(client_socket)
            
            if not new_name:
                fault_msg = wrap_send_msg("Can't create the room.")
                client_socket.send(bytes(fault_msg))
                user = receive_message(client_socket)
                continue
            
            uniq_name = True
            for rm in rooms:
                if rm == new_name:
                    uniq_name = False
                    break
                
            if not uniq_name:
                fault_msg = wrap_send_msg(f"The room {new_name} already exists.")
                client_socket.send(bytes(fault_msg))
                user = receive_message(client_socket)
                continue
            
            rooms[new_name] = {"sockets":[server_socket, client_socket], "history": [], "names":[username]}
        
            print(f"room {new_name} created.")
            result = True
            #print(rooms)
            break
        elif user_ans == "\sub":
            print("uh he wants in a room")
            target = get_room_name(client_socket)
            if not target:
                client_socket.send(bytes(wrap_send_msg(f"Cant connect.")))
                user = receive_message(client_socket)
                continue
            if not target in rooms:
                client_socket.send(bytes(wrap_send_msg(f"No room named {target}.")))
                user = receive_message(client_socket)
                continue                
            uniq_name = True
            for nm in rooms[target]["names"]:
                if username == nm:
                    uniq_name = False
                    break
            if not uniq_name:
                client_socket.send(bytes(wrap_send_msg(f"User with '{username}' name is already in the room.")))
                user = receive_message(client_socket)
                continue 
            
            rooms[target]["sockets"].append(client_socket)
            rooms[target]["names"].append(username)
            #sending history...
            return True
    

        elif user_ans == "\exit":
            return False #break
        else:
            default_msg = wrap_send_msg("No such option")
            client_socket.send(bytes(default_msg))
            user = receive_message(client_socket)
    
    return result
                
    
     
    
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    #print(rooms)
    
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            
            client_socket, client_address = server_socket.accept()
        
        
            user = receive_message(client_socket)
            
            if user == False:
                continue
            
            sockets_list.append(client_socket)
            
            clients[client_socket] = user
            
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username {user['data'].decode('utf-8')}")    
            
            connected = connect_client(user, client_socket, server_socket, rooms)
            print("ok ----- roommm  got him")
            if connected:
                sockets_list.append(client_socket)
                client_socket.send(bytes(wrap_send_msg("connected")))
                               
        else:
            message = receive_message(notified_socket)
            
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            user = clients[notified_socket]
            
            
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    
                    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]