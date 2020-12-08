from app.config import AVAILABLE_COMMANDS


def list_commands():
    message_header = ['Unknown command. Available commands are:']
    commands_list = [
        f'\t{command} - {description}'
        for command, description in AVAILABLE_COMMANDS.items()
    ]

    return '\n'.join(message_header + commands_list)
