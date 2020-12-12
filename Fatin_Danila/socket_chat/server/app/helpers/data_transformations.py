import json
import re


def get_input_data(encoded_string):
    decoded_string = encoded_string.decode()
    # let's use }{ as separator to prevent reading multiple jsons as one
    messages = re.split('}{', decoded_string)
    reconstructed_messages = []
    for message in messages:
        if message != '}{':
            if '{' not in message:
                message = '{' + message
            if '}' not in message:
                message = message + '}'
            reconstructed_messages.append(message)

    input_data = []
    for message in reconstructed_messages:
        # check if message is a valid json
        try:
            proccessed_message = json.loads(message)
            input_data.append(proccessed_message)
        except json.decoder.JSONDecodeError:
            pass

    return input_data


def get_output_data(message_dict):
    output_json = json.dumps(message_dict)

    return output_json.encode()
