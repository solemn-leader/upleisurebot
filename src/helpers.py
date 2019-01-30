import random
from models import User, Event
from vk_api.longpoll import VkEventType
from access_token import TOKEN
import vk_api

API = vk_api.VkApi(token=TOKEN)
# API_methods = API.get_api()

CHAT_STATUSES = {
    'JUST_STARTED': 0,  # user has seen initial message
    'SEEN_EVENT': 1,  # user has seen other user's event
    'USER_HAS_LEFT_FEEDBACK1': 2  # user has left feedback
}


def __get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])


def __get_user_name(user_id):
    user = API.method(
        'users.get',
        {
            'user_ids': user_id
        }
    )[0]
    return user['first_name'] + ' ' + user['last_name']


def __write_msg(user_id, text, attachments='photo-36147615_456275469'):
    API.method(
        'messages.send',
        {
            'user_id': user_id,
            'message': text,
            'random_id': __get_random_id(),
            'attachment': attachments
        }
    )


def __get_chat_status(event: VkEventType.MESSAGE_NEW) -> int:
    if User.select().where(User.pk == event.user_id).exists():
        pass  # get chat status
    else:
        __create_new_user(event.user_id, __get_user_name(event.user_id))
        return CHAT_STATUSES['JUST_STARTED']


def __create_new_user(user_id, name) -> User:
    return User.create(
        pk=user_id,
        name=name,
        chat_status=CHAT_STATUSES['JUST_STARTED']
    )


# all the logic actually happens here
def __what_should_bot_respond(event: VkEventType.MESSAGE_NEW) -> (str, str):
    chat_status = __get_chat_status(event)
    if chat_status == CHAT_STATUSES['JUST_STARTED']:
        text = 'Что будем делать?'
        attachments = ''
    else:
        text = 'Я забыл, о чем мы говорили :('
        attachments = ''
    return (text, attachments)


def make_bot_response(event: VkEventType.MESSAGE_NEW):
    text, attachments = __what_should_bot_respond(event)
    __write_msg(
        event.user_id,
        text,
        attachments
    )
