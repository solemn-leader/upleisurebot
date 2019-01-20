import random


def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])


def write_msg(api, user_id, message):
    api.method(
        'messages.send', 
        {
            'user_id': user_id, 
            'message': message, 
            'random_id': get_random_id()
        }
    )
