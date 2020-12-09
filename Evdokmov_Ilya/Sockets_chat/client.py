import socket
import select
import errno
import sys
import time

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3000

my_username = input("Username: ")
client_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_soket.connect((IP, PORT))
client_soket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_soket.send(username_header + username)

def wrap_send_msg(message):
    msg_header = f"{len(message):< {HEADER_LENGTH}}".encode("utf-8")
    return msg_header + message.encode("utf-8")

connected = False
while not connected:
    try:
        server_header = client_soket.recv(HEADER_LENGTH)
        server_length = int(server_header.decode("utf-8"))
        server = client_soket.recv(server_length).decode("utf-8")   
        
        print(f"{server}")
        
        if server == "connected":
            print("loading history of room")
            time.sleep(1)
            #print_history()
            print("printed")
            connected = True
            break
            
        message = input(f"{my_username} (not active)>") 
        if message:
            message = message.encode("utf-8")
            message_header = f"{len(message):< {HEADER_LENGTH}}".encode("utf-8")
            client_soket.send(message_header + message)
    
        
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue
            
    except Exception as e:
        print("General error", str(e))
        sys.exit()    
    


while True:
    message = input(f"{my_username}  > ")
    
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