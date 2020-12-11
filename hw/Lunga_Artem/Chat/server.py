import socket

SERVER_ADDRESS = ('localhost', 8125)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(SERVER_ADDRESS)
clients = []
members = {}
room_story = []
ROOM = ""
print("Server is running")

def registration(port_address):

    rooms_data = 'Необходимо выбрать комнату, введите room1, room2, room3'
    server_socket.sendto(rooms_data.encode('utf-8'), address)
        
    def confirm_rooms_1(port_address):
        name, address = server_socket.recvfrom(1024)
        if (name.decode('utf-8') == "room1" or name.decode('utf-8') == "room2" 
            or name.decode('utf-8') == "room3"):
            global ROOM
            ROOM = name.decode('utf-8')
            enter = "Вы вошли в " + name.decode('utf-8')
            server_socket.sendto(enter.encode('utf-8'), address)
        else:
            no_enter = "Введённое значение некорректно"
            server_socket.sendto(no_enter.encode('utf-8'), address)
            uncorrect_room(port_address)
            
    def uncorrect_room(port_address):
        rooms_data = 'Необходимо выбрать комнату, введите room1, room2, room3'
        server_socket.sendto(rooms_data.encode('utf-8'), port_address)
        confirm_rooms_1(port_address)

    confirm_rooms_1(port_address)
    
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

INDEX = 0
FLAG = False

while True:
    data, address = server_socket.recvfrom(1024)
    print(address[0], address[1])
    if address not in clients:
        clients.append(address)
        registration(address)
        text = ("Добро пожаловать в чат!\n" +
                "Вы можете посмотреть историю чата, если напишите 'story'.\n" +
                "Вы можете сменить комнату, если напишите 'room'\n" +
                "С помощью команды 'room' вы сожете перезайти в комнату" +
                "Вы можете выйти, если введёте 'Ctrl + C'")
        server_socket.sendto(text.encode('utf-8'), address)

    for client in clients:

        if client == address:
            text_from_client = data.decode('utf-8')
            room_story.append(text_from_client)
            
            print ("[" + members + ", " + ROOM + "]")
            
            if (text_from_client == "room"):
                INDEX = len(room_story)
                FLAG = True
                registration(address)
                text = ("Добро пожаловать в чат!\n" +
                        "Вы можете посмотреть историю чата, если напишите 'story'.\n" +
                        "Вы можете сменить комнату, если напишите 'room'\n" +
                        "С помощью команды 'room' вы сожете перезайти в комнату" +
                        "Вы можете выйти, если введёте 'Ctrl + C'")
                server_socket.sendto(text.encode('utf-8'), address)
                text_from_client = data.decode('utf-8')                
            
            if (text_from_client != "story" and text_from_client != "Story" 
                and text_from_client != "room"):
                print(text_from_client)
        
                
            if (text_from_client == "story" or text_from_client == "Story"):
                print("История чата:")
                if (FLAG):
                    if text_from_client == "Story":
                        room_story.insert(1, 'story')
                    if text_from_client == "story":
                        room_story.insert(1, 'Story')
                    room_story.remove('story')
                    room_story.remove('Story')
                    print (room_story[INDEX::])
                else:
                    room_story.remove('Connect to server')
                    if text_from_client == "Story":
                        room_story.insert(1, 'story')
                    if text_from_client == "story":
                        room_story.insert(1, 'Story')
                    room_story.remove('story')
                    room_story.remove('Story')
                    print(room_story)
                    room_story.insert(1,'Connect to server')
            
            continue

        server_socket.sendto(data, client)
