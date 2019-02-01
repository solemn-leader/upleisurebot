import random
from models import User, Event
from vk_api.longpoll import VkEventType, Event
from access_token import TOKEN
import vk_api
from consts import *
from get_response import *
from helpers import *

API = vk_api.VkApi(token=TOKEN)


def __handle_feedback(text, user_id) -> (str, str, str):
    '''return message, attachments and new chat_status'''
    if text == '0':
        message = CANCEL_SEND_FEEDBACK_MESSAGE
    elif len(text) < 6:
        message = FEEDBACK_TOO_SMALL_MESSAGE
    else:
        message = THANK_FOR_FEEDBACK_MESSAGE
        # save feedback
    return(
        message,
        '',
        ChatStatuses.SELECTS_WHAT_TO_DO
    )


def __handle_event(text, attachments, user_id) -> (str, str, str):
    '''return message, attachments and new chat_status'''
    if text == '0':
        message = CANCEL_SEND_EVENT_MESSAGE
    elif (len(text) < 6 and attachments == ''):
        message = EVENT_TOO_SMALL_MESSAGE
    else:
        message = EVENT_ACCEPTED_MESSAGE
        # save event
    return(
        message,
        '',
        ChatStatuses.SELECTS_WHAT_TO_DO
    )


def __get_user_info(user_id) -> (str, str, int):
    '''returns vk full name, city, and age by vk id'''
    user = API.method(
        'users.get',
        {
            'user_ids': user_id
        }
    )[0]
    name = user['first_name'] + ' ' + user['last_name']
    if 'city' not in user.keys():  # user has not set city
        city = ''
    else:
        city = user['city']['title']
    if 'bdate' not in user.keys():  # user has not set city
        age = -1
    else:
        age = get_age_from_birth(user['bdate'])
    return (name, city, age)


def __write_msg(user_id, text, attachments='photo-36147615_456275469'):
    '''sends message to user'''
    API.method(
        'messages.send',
        {
            'user_id': user_id,
            'message': text,
            'random_id': get_random_id(),
            'attachment': attachments
        }
    )


def __get_chat_status(event: Event) -> int:
    if User.select().where(User.pk == event.user_id).exists():
        return User.get(User.pk == event.user_id).chat_status
    else:
        user_date = __get_user_info(event.user_id)
        if ('' in user_date) or (-1 in user_date):
            return ChatStatuses.USER_MUST_SET_CITY_OR_AGE
        __create_new_user(event.user_id, *__get_user_info(event.user_id))
        return ChatStatuses.JUST_STARTED


def __set_chat_status(event: Event, new_status: int):
    User.update({User.chat_status: new_status}) \
        .where(User.pk == event.user_id).execute()


def __create_new_user(user_id, name, city, age) -> User:
    return User.create(
        pk=user_id,
        name=name,
        chat_status=ChatStatuses.SELECTS_WHAT_TO_DO,
        city=city,
        age=AgeGroups.get_age_group(age)
    )


# all the logic actually happens here
def __what_should_bot_respond(event: Event) -> (str, str):
    chat_status = __get_chat_status(event)
    user_reply = event.text
    attachments = ''
    messages = []  # we return this
    print(chat_status)
    if chat_status == ChatStatuses.JUST_STARTED:
        response_text, attachments, \
            new_chat_status = get_response_just_started()

    elif chat_status == ChatStatuses.SEEN_EVENT:
        response_text, attachments, new_chat_status = get_response_seen_event(
            user_reply,
            event.user_id
        )

    elif chat_status == ChatStatuses.WANTS_TO_SEND_EVENT:
        response_text, attachments, new_chat_status = __handle_event(
            event.text,
            event.attachments,
            event.user_id
        )

    elif chat_status == ChatStatuses.WANTS_TO_SEND_FEEDBACK:
        response_text, attachments, new_chat_status = __handle_feedback(
            event.text,
            event.user_id
        )

    elif chat_status == ChatStatuses.SELECTS_WHAT_TO_DO:
        response_text, attachments,\
            new_chat_status = get_response_selected_what_to_do(
                user_reply,
                event.user_id
            )

    else:
        response_text = 'Я забыл, о чем мы говорили :('
        attachments = ''
        new_chat_status = ChatStatuses.SELECTS_WHAT_TO_DO
    messages.append((response_text, attachments))
    # if user reply was valid and it was not first message
    if (response_text != DID_NOT_GET_IT_MESSAGE) and \
       (chat_status != ChatStatuses.JUST_STARTED) and \
       (chat_status != ChatStatuses.USER_MUST_SET_CITY_OR_AGE):
        if new_chat_status == ChatStatuses.SEEN_EVENT:
            if False:  # here we should check if there are events to show
                pass  # otherwise we should set SELECT WHAT TO DO
            else:
                messages.append((MAKE_SEEN_EVENT_CHOICES_MESSAGE, ''))
        elif new_chat_status == ChatStatuses.SELECTS_WHAT_TO_DO:
            messages.append((SELECT_WHAT_TO_DO_CHOICES_MESSAGE, ''))

        __set_chat_status(event, new_chat_status)
    return messages


def make_bot_response(event: Event):
    if event.user_id in PEOPLE_WHO_ARE_ALLOWED_TO_WRITE:
        for text, attachments in __what_should_bot_respond(event):
            __write_msg(
                event.user_id,
                text,
                attachments
            )
