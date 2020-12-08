# SERVER_HOST = '192.168.0.106'
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

ALLOWED = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-"

ROOM_STORY_LENGTH = 128

COMMANDS = {
    '/create [roomname]': 'create room',
    '/rooms [key or none]': 'list of rooms, flags: -all, -my',
    '/sub [roomname] as [nickname]': 'subscribe the room',
    '/join [roomname]': 'join to the room',
    '/quit': 'quit from current room',
    '/clear' : 'clear console'
} 