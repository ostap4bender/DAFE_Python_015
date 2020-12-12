def event(event_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if isinstance(response, dict):
                if 'event' not in response:
                    response['event'] = event_name
            elif isinstance(response, list):
                for msg in response:
                    if 'event' not in msg:
                        msg['event'] = event_name

            return response
        return wrapper
    return decorator


def sign_response(signature):
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if isinstance(response, dict):
                if 'author' not in response:
                    response['author'] = signature
            elif isinstance(response, list):
                for msg in response:
                    if 'author' not in msg:
                        msg['author'] = signature

            return response
        return wrapper
    return decorator
