SERVER_HOST = '192.168.0.17'
SERVER_PORT = 65432

ROOM_STORY_LENGTH = 128

COMMANDS = {
    '/create': 'create room (params: name)',
    '/ls': 'list of rooms (flags: -all, -my)',
    '/sub': 'subscribe the room (params: name, nick)',
    '/join': 'join to the room (params: name)',
    '/quit': 'quit from current room',
    '/exit': 'exit from chat'
}