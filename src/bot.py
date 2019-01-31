import random
from models import User, Event
from vk_api.longpoll import VkEventType
from access_token import TOKEN
import vk_api
from consts import *
from get_response import *

API = vk_api.VkApi(token=TOKEN)


def __handle_feedback(text, user_id):
    pass


def __handle_event(text, attachments, user_id):
    pass


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


def __set_chat_status(event: VkEventType.MESSAGE_NEW, new_status: int):
    User.update({User.chat_status: new_status}) \
        .where(User.pk == event.user_id).execute()


def __create_new_user(user_id, name) -> User:
    return User.create(
        pk=user_id,
        name=name,
        chat_status=CHAT_STATUSES['JUST_STARTED']
    )


# all the logic actually happens here
def __what_should_bot_respond(event: VkEventType.MESSAGE_NEW) -> (str, str):
    chat_status = __get_chat_status(event)
    user_choice = event.text
    attachments = ''
    messages = []  # we return this
    if chat_status == CHAT_STATUSES['JUST_STARTED']:
        response_text, attachments, \
            new_chat_status = get_response_just_started(
                user_choice,
                event.user_id
            )

    elif chat_status == CHAT_STATUSES['MAKES_EVENT_CHOICE']:
        response_text, attachments, \
            new_chat_status = get_response_seen_event(
                user_choice,
                event.user_id
            )

    elif chat_status == CHAT_STATUSES['WANTS_TO_SEND_EVENT']:
        __handle_event(
            event.text,
            event.attachments,
            event.user_id
        )
        response_text, attachments, \
            new_chat_status = get_response_just_started(
                user_choice,
                event.user_id
            )

    elif chat_status == CHAT_STATUSES['SELECTS_WHAT_TO_DO']:
        response_text, attachments, \
            new_chat_status = get_response_just_started(
                user_choice,
                event.user_id
            )

    elif chat_status == CHAT_STATUSES['WANTS_TO_SEND_FEEDBACK']:
        __handle_feedback(
            event.text,
            event.user_id
        )

        response_text, attachments, \
            new_chat_status = get_response_just_started(
                user_choice,
                event.user_id
            )

    else:
        response_text = 'Я забыл, о чем мы говорили :('
        attachments = ''
    messages.append((response_text, attachments))
    if response_text != DID_NOT_GET_IT_MESSAGE:  # if user's respond was valid
        if new_chat_status == CHAT_STATUSES['MAKES_EVENT_CHOICE']:
            if False:  # here we should check if there are events to show
                pass  # otherwise we should set SELECT WHAT TO DO
            else:
                messages.append((MAKE_SEEN_EVENT_CHOICES_MESSAGE, ''))
        elif new_chat_status == CHAT_STATUSES['SELECTS_WHAT_TO_DO']:
            messages.append(SELECT_WHAT_TO_DO_CHOICES_MESSAGE, '')
        
        __set_chat_status(event, new_chat_status)
    return messages


def make_bot_response(event: VkEventType.MESSAGE_NEW):
    for text, attachments in __what_should_bot_respond(event):
        __write_msg(
            event.user_id,
            text,
            attachments
        )
