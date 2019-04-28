import random

import vk_api
from vk_api.longpoll import Event, VkEventType

from access_token import TOKEN
from consts import *
from get_response import *
from helpers import *
from models import TeenEvent, User, YoungEvent

API = vk_api.VkApi(token=TOKEN)


def everyone_allowed(list_of_all_users):
    return (len(list_of_all_users) != 0) and list_of_all_users[0] == 1


def __handle_feedback(text, user_id) -> (str, str, str):
    '''return message, attachments and new chat_status
    func is called when user sends feedback'''
    if text == '0':  # 0 meand user has canceled
        message = CANCEL_SEND_FEEDBACK_MESSAGE

    elif len(text) < 6:  # if feedack is too short
        message = FEEDBACK_TOO_SMALL_MESSAGE

    else:  # feedback is alright
        message = THANK_FOR_FEEDBACK_MESSAGE
        # send feedback to me
        __write_msg(
            MY_ID,
            "FEEDBACK:\n" + text,
            ''
        )

    return(
        message,
        '',
        ChatStatuses.SELECTS_WHAT_TO_DO
    )


def __handle_sent_event(text, attachments, user_id) -> (str, str, str):
    '''return message, attachments and new chat_status
    func is called when user has sent event'''
    if text == '0':  # 0 meand user has canceled
        message = CANCEL_SEND_EVENT_MESSAGE

    elif (len(text) < 6) and (not attachments):  # event is too small
        message = EVENT_TOO_SMALL_MESSAGE

    else:
        message = EVENT_ACCEPTED_MESSAGE
        # save event
        user = User.get(User.user_id == user_id)
        if user.age_group == AgeGroups.TEENS:
            event_class = TeenEvent
        else:
            event_class = YoungEvent
        event_class.create(
            city=user.city,
            description=text,
            attachments=attachments,
            owner=user
        )

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
            'user_ids': user_id,
            'fields': 'city, bdate'
        }
    )[0]
    name = user['first_name'] + ' ' + user['last_name']
    if 'city' not in user.keys():  # user has not set city
        city = ''
    else:
        city = user['city']['title']
    if 'bdate' not in user.keys():  # user has not set age
        age = -1
    else:
        age = get_age_from_birth(user['bdate'])
    return (name, city, age)


def __write_msg(user_id, text, attachments='photo-36147615_456275469'):
    '''sends message to user with vk id = user_id'''
    API.method(
        'messages.send',
        {
            'user_id': user_id,
            'message': text,
            'random_id': get_random_id(),
            'attachment': attachments
        }
    )


def __get_chat_status(user_id) -> int:
    '''gets chat status for user with such id (creates new if not exists)'''
    if User.select().where(User.user_id == user_id).exists():
        return User.get(User.user_id == user_id).chat_status
    else:
        name, city, age = __get_user_info(user_id)
        if ('' == city) or (-1 == age):  # user has no age or city
            return ChatStatuses.USER_MUST_SET_CITY_OR_AGE
        else:
            __create_new_user(user_id, name, city, age)
            return ChatStatuses.JUST_STARTED


def __set_chat_status(user_id, new_status: int):
    '''sets chat user for user with such user_id'''
    if new_status != -1:  # if status is -1 we must not set it
        if User.select().where(User.user_id == user_id).exists():
            User.update({User.chat_status: new_status}) \
                .where(User.user_id == user_id).execute()


def __create_new_user(user_id, name, city, age) -> User:
    '''creates new user'''
    return User.create(
        user_id=user_id,
        name=name,
        # user at once selects what to do, JUST_STARTED is never set
        chat_status=ChatStatuses.SELECTS_WHAT_TO_DO,
        city=city,
        age_group=AgeGroups.get_age_group(age)
    )


# all the logic actually happens here
def __what_should_bot_respond(event: Event) -> [(str, str), (str, str)]:
    '''this func returns rray of (message, attachments), handles user respond
    and sets chat statuses'''
    chat_status = __get_chat_status(event.user_id)
    user_reply = event.text
    messages = []  # we return this
    if chat_status == ChatStatuses.JUST_STARTED:
        response_text, attachments, \
            new_chat_status = get_response_just_started()

    elif chat_status == ChatStatuses.SEEN_EVENT:
        response_text, attachments, new_chat_status = get_response_seen_event(
            user_reply,
            event.user_id
        )

    elif chat_status == ChatStatuses.WANTS_TO_SEND_EVENT:
        response_text, attachments, new_chat_status = __handle_sent_event(
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

    elif chat_status == ChatStatuses.USER_MUST_SET_CITY_OR_AGE:
        response_text, attachments,\
            new_chat_status = get_response_user_must_set_city_or_age()

    else:  # something went wrong
        response_text = 'Я забыл, о чем мы говорили :('
        attachments = ''
        new_chat_status = ChatStatuses.SELECTS_WHAT_TO_DO

    messages.append((response_text, attachments))

    # if user reply was valid and
    # his profile is valid we might also set new chat status
    # and send some more messages
    if (response_text != DID_NOT_GET_IT_MESSAGE) and \
       (chat_status != ChatStatuses.USER_MUST_SET_CITY_OR_AGE):

        if new_chat_status == ChatStatuses.SEEN_EVENT:

            # we check if there is no passed event
            if response_text == NO_EVENTS_MESSAGE:
                # set SELECT WHAT TO DO status and send choices in such case
                new_chat_status = ChatStatuses.SELECTS_WHAT_TO_DO
                messages.append((SELECT_WHAT_TO_DO_CHOICES_MESSAGE, ''))

            else:
                # otherwise we must also send choices for user for this event
                messages.append((MAKE_SEEN_EVENT_CHOICES_MESSAGE, ''))

        elif new_chat_status in (ChatStatuses.JUST_STARTED,
                                 ChatStatuses.SELECTS_WHAT_TO_DO):
            messages.append((SELECT_WHAT_TO_DO_CHOICES_MESSAGE, ''))

        __set_chat_status(event.user_id, new_chat_status)

    return messages


def make_bot_response(event: Event):
    '''this function makes bot respond!'''
    if everyone_allowed(PEOPLE_WHO_ARE_ALLOWED_TO_WRITE) or \
        (event.user_id in PEOPLE_WHO_ARE_ALLOWED_TO_WRITE):
        for text, attachments in __what_should_bot_respond(event):
            __write_msg(
                event.user_id,
                text,
                attachments
            )
