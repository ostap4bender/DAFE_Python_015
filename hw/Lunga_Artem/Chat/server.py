import socket

SERVER_ADDRESS = ('localhost', 8125)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(SERVER_ADDRESS)
clients = []
members = {}
print("Server is running")

def registration(port_address):
    register_data = 'Необходимо пройти регистрацию, введите свой ник: '
    server_socket.sendto(register_data.encode('utf-8'), address)

    def confirm_nickname(port_address):
        name, address = server_socket.recvfrom(1024)
        registration_data = f"Ваш ник {name.decode('utf-8')}? Введите yes или no."
        server_socket.sendto(registration_data.encode('utf-8'), address)
        append_to_list(name, port_address)

    def new_nickmane(address):
        registration_data = 'Введите свой ник: '
        server_socket.sendto(registration_data.encode('utf-8'), address)
        confirm_nickname(address)

    def append_to_list(name, port_address):
        data, address = server_socket.recvfrom(1024)
        if (data.decode('utf-8') == 'Yes' or data.decode('utf-8') == 'yes'):
            get_pass(name)
        else:
            new_nickmane(port_address)

    def get_pass(name):
        pass_data_1 = "Введите пароль для своего ника: "
        server_socket.sendto(pass_data_1.encode('utf-8'), address)
        password_1, adr= server_socket.recvfrom(1024)
        pass_data_2 = "Повторите пароль:"
        server_socket.sendto(pass_data_2.encode('utf-8'), address)
        password_2, adr = server_socket.recvfrom(1024)

        if password_1 == password_2:
            global members
            members = name.decode('utf-8')
            pass_data_3 = "Отлично, регистрация прошла успешно!"
            server_socket.sendto(pass_data_3.encode('utf-8'), address)
        else:
            pass_data_4 = "Попробуйте снова:"
            server_socket.sendto(pass_data_4.encode('utf-8'), address)
            get_pass(name)

    confirm_nickname(port_address)

p = []

while True:
    data, address = server_socket.recvfrom(1024)
    print(address[0], address[1])
    if address not in clients:
        clients.append(address)
        registration(address)
        text = "Добро пожаловать в чат!\nВы можете посмотреть историю чата, если напишите 'story'."
        server_socket.sendto(text.encode('utf-8'), address)

    for client in clients:

        if client == address:
            text_from_client = data.decode('utf-8')
            p.append(text_from_client)
            print ("[" + members + "]")
            if (text_from_client != "story" and text_from_client != "Story"):
                print(text_from_client)
            if (text_from_client == "story" or text_from_client == "Story"):
                print("Story of chat:")
                p.remove('Connect to server')
                if text_from_client == "Story":
                    p.insert(1, 'story')
                if text_from_client == "story":
                    p.insert(1, 'Story')
                p.remove('story')
                p.remove('Story')
                print(p)
                p.insert(1,'Connect to server')
            
            continue

        server_socket.sendto(data, client)