CHAT_STATUSES = {
    'JUST_STARTED': 0,  # user has seen initial message
    'SEEN_EVENT': 1,  # user has seen other user's event
    'WANTS_TO_LEAVE_EVENT': 2,
    'WANTS_TO_LEAVE_FEEDBACK': 3,  # user has left feedback
    'SELECT_WHAT_TO_DO': 4
}

DID_NOT_GET_IT_MESSAGE = 'Извиняюсь, не совсем понял вас.'

SEND_EVENT_MESSAGE = '''Окей, отправь мне описание события, и фоточки.
 Отправь 0(нулик) для отмены. '''

SEND_FEEDBACK_MESSAGE = '''Окей, скажи мне, что тебе не нравится в боте
 и что можно исправить. Отправь 0(нулик) для отмены.'''

THANK_FOR_FEEDBACK_MESSAGE = '''Спасибо за обратную связь. Мы это ценим!'''

EVENT_ACCEPTED_MESSAGE = '''Твоя заявка принята!'''

JUST_STARTED_CHOICES = {
    'Смотреть заявки других': 1,
    'Оставить заявку': 2
}

JUST_STARTED_CHOICES_MESSAGE = '\n'.join(
    ['{} - {}'.format(key, value) for key, value in JUST_STARTED_CHOICES]
    )

SEEN_EVENT_CHOICES = {
    'Мне нравится это предложение!': 1,
    'Покажи мне другое': 2,
    'Хочу оставить заявку': 3,
    'Хочу оставить фидбэк': 4
}

MAKE_SEEN_EVENT_CHOICES_MESSAGE = '\n'.join(
    ['{} - {}'.format(key, value) for key, value in SEEN_EVENT_CHOICES]
    )

SELECT_WHAT_TO_DO_CHOICES = {
    'Смотреть заявки других': 1,
    'Оставить заявку': 2,
    'Оставить фидбэк': 3
}

SELECT_WHAT_TO_DO_CHOICES_MESSAGE = '\n'.join(
    ['{} - {}'.format(key, value) for key, value in SELECT_WHAT_TO_DO_CHOICES]
    )
