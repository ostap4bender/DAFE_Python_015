AVAILABLE_COMMANDS = {
    '/create_profile': 'Register, signature: /create_profile <login> <password>',
    '/auth': 'Authenticate, signature: /auth <login> <password>',
    '/create_room': 'Create chat room, signature: /create_room <room_title> <nickname (optional)>',
    '/subscribe': 'Subscribe to chat room, signature: /subscribe <room_title> <nickname (optional)>',
    '/unsubscribe': 'Unsubscribe from chat room, signature: /unsubscribe <room_title>',
    '/join': 'Join chat room, signature: /join <room_title>',
    '/rooms': 'Show rooms, available optional params: --my, --current',
    '/quit': 'Quit current chat room',
    '/logout': 'Logout',
    '/shutdown': 'Go offline',
    '/poweron': 'Go online',
    '/help': 'help',
}

SERVER_SIGNATURE = 'Server'
