from consts import *
from helpers import get_event_for_user, user_liked_event_get_response


'''All funcs starting with 'get_rseponse'
return message, attachments and new chat_status'''


def get_response_just_started() -> (str, str, int):
    '''when user has just started chat'''
    message = INITIAL_MESSAGE
    attachments = ''
    new_chat_status = ChatStatuses.SELECTS_WHAT_TO_DO
    return (message, attachments, new_chat_status)


def get_response_seen_event(user_choice, user_id) -> (str, str, int):
    '''user has seen event and has made his choice'''
    if (not user_choice.isdigit()) or \
       (int(user_choice) not in SEEN_EVENT_CHOICES.values()):
        # user input is invalid
        return (
            DID_NOT_GET_IT_MESSAGE,
            '',
            -1
        )

    else:
        user_choice = int(user_choice)
        if user_choice == SEEN_EVENT_CHOICES['Мне нравится это предложение!']:
            message, attachments = user_liked_event_get_response(user_id)
            return (
                message,
                attachments,
                ChatStatuses.SELECTS_WHAT_TO_DO
            )

        elif user_choice == SEEN_EVENT_CHOICES['Покажи мне другое']:
            message, attachments = get_event_for_user(user_id)
            return (
                message,
                attachments,
                ChatStatuses.SEEN_EVENT
            )

        elif user_choice == SEEN_EVENT_CHOICES['Хочу оставить заявку']:
            return (
                SEND_EVENT_MESSAGE,
                '',
                ChatStatuses.WANTS_TO_SEND_EVENT
            )

        elif user_choice == SEEN_EVENT_CHOICES['Хочу оставить фидбэк']:
            return (
                SEND_FEEDBACK_MESSAGE,
                '',
                ChatStatuses.WANTS_TO_SEND_FEEDBACK
            )


def get_response_selected_what_to_do(user_choice, user_id) -> (str, str, int):
    '''user has selected what to do'''
    if (not user_choice.isdigit()) or \
       (int(user_choice) not in SELECT_WHAT_TO_DO_CHOICES.values()):
        # user input is invalid
        return (DID_NOT_GET_IT_MESSAGE, '', '')

    else:
        user_choice = int(user_choice)
        if user_choice == SELECT_WHAT_TO_DO_CHOICES['Смотреть заявки других']:
            message, attachments = get_event_for_user(user_id)
            return (
                message,
                attachments,
                ChatStatuses.SEEN_EVENT
            )

        elif user_choice == SELECT_WHAT_TO_DO_CHOICES['Оставить заявку']:
            return (
                SEND_EVENT_MESSAGE,
                '',
                ChatStatuses.WANTS_TO_SEND_EVENT
            )

        elif user_choice == SELECT_WHAT_TO_DO_CHOICES['Оставить фидбэк']:
            return (
                SEND_FEEDBACK_MESSAGE,
                '',
                ChatStatuses.WANTS_TO_SEND_FEEDBACK
            )


def get_response_user_must_set_city_or_age() -> (str, str, int):
    '''call this func when user has no city or age on vk'''
    message = USER_MUST_SET_CITY_OR_AGE_MESSAGE
    attachments = ''
    new_chat_status = -1
    return (message, attachments, new_chat_status)
