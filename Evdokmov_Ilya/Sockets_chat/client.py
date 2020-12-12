import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3000


KEYWORD_DICONNECT = "00934283979723"
KEYWORD_CREATE = "0000983275890"
KEYWORD_SWITCH = "3275927034523"
KEYWORD_SUB = "0094723443045"

my_username = input("Username: ")
client_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_soket.connect((IP, PORT))
client_soket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_soket.send(username_header + username)


optional_comands = ["\create  -  to create a room", "\sub - to subscribe to existing room",
                    "\switch  -  to start texting to another room", "\see - to see existing rooms",
                    "\cnclsub - to cancel sub", "\exit  -  to leave the server"]

welcome_message = f"Hi, {username.decode('utf-8')}!\nYou've connected to the soket-chat server!\nOptional commands:\n"
for cmd in optional_comands:
    welcome_message += (cmd + '\n')
welcome_message += "\n!! devide command and roomname by space.\n" #(comands works for rooms only if you input nameroom after command)
#welcome_message += "Rules: no empty messages (after sending them you became banned)\n"
print(welcome_message)


connected = True
current_room = "default"
while True:
    if not connected:
        print("~disconnected")
        break
    message = input(f"[{current_room}]{my_username} > ")
    
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):< {HEADER_LENGTH}}".encode("utf-8")
        client_soket.send(message_header + message)
    
    try:
        while True:
            #receive things
            username_header = client_soket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()
                
            username_length = int(username_header.decode("utf-8"))
            username = client_soket.recv(username_length).decode("utf-8")
            
            if username == KEYWORD_DICONNECT:
                connected = False
                continue
            
            if len(username) > len(KEYWORD_CREATE):
                
                if username[:len(KEYWORD_CREATE)] == KEYWORD_CREATE:
                    current_room = username[len(KEYWORD_CREATE):]
                    print(current_room, " room created.")
                    continue
            if len(username) > len(KEYWORD_SWITCH):
                if username[:len(KEYWORD_SWITCH)] == KEYWORD_SWITCH:
                    current_room = username[len(KEYWORD_CREATE):]
                    print(f"switched to {current_room}.")
                    continue  
            if len(username) > len(KEYWORD_SUB):
                if username[:len(KEYWORD_SUB)] == KEYWORD_SUB:
                    sub_room_hist = username[len(KEYWORD_SUB):]
                    print(sub_room_hist)
                    continue                 
            
            
            message_header = client_soket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8"))
            message = client_soket.recv(message_length).decode("utf-8")
            
            print(f"{username} > {message}")
            
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue
            
    except Exception as e:
        print("General error", str(e))
        sys.exit()