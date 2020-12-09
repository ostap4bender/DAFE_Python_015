import socket
import threading

SERVER_ADDRESS = ('localhost', 8125)
sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sor.bind(('', 0))
sor.sendto(('Connect to server').encode('utf-8'), SERVER_ADDRESS)

def reading_socket():
    while True:
        data = sor.recv(1024)
        print(data.decode('utf-8'))


potok = threading.Thread(target=reading_socket)
potok.start()

s = []

while True:
    message = input()
    sor.sendto((message).encode('utf-8'), SERVER_ADDRESS)