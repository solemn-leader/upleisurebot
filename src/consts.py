import datetime

MY_ID = 210045485


class ChatStatuses:
    JUST_STARTED = 0  # this can only be returned when user starts chat

    SEEN_EVENT = 1  # user has seen other user's event

    WANTS_TO_SEND_EVENT = 2

    WANTS_TO_SEND_FEEDBACK = 3  # user has left feedback

    SELECTS_WHAT_TO_DO = 4

    USER_MUST_SET_CITY_OR_AGE = 5


class AgeGroups:
    TEENS = 0
    TEENS_BOUNDS = (1, 17)
    YOUNG = 1
    YOUNG_BOUNDS = (18, 80)

    @staticmethod
    def get_age_group(age: int) -> int:
        if AgeGroups.TEENS_BOUNDS[0] <= age <= AgeGroups.TEENS_BOUNDS[1]:
            return AgeGroups.TEENS
        else:
            return AgeGroups.YOUNG


PEOPLE_WHO_ARE_ALLOWED_TO_WRITE = [
    210045485
]

USER_MUST_SET_CITY_OR_AGE_MESSAGE = '''Упс :( чтобы пользоваться ботом нужно указать в профиле
город и возраст
'''

NO_EVENTS_MESSAGE = '''
Упс... Нам нечего показать( Но это не страшно, ты можешь сам оставить заявку!
'''

DID_NOT_GET_IT_MESSAGE = 'Извиняюсь, не совсем понял вас.'

SEND_EVENT_MESSAGE = '''Окей, отправь мне описание события, и фоточки.
 Отправь 0(нулик) для отмены. '''

SEND_FEEDBACK_MESSAGE = '''Окей, скажи мне, что тебе не нравится в боте
 и что можно исправить. Отправь 0(нулик) для отмены.
 P.S.
 все заявки действуют втечение пяти суток'''

FEEDBACK_TOO_SMALL_MESSAGE = '''Твой фидбэк был слишком маленьким :('''

EVENT_TOO_SMALL_MESSAGE = '''Твоя заявка слишком маленькая :('''

CANCEL_SEND_EVENT_MESSAGE = '''Окей, ты отменил свою заявку.
'''

CANCEL_SEND_FEEDBACK_MESSAGE = '''Окей, ты отменил отправку фидбэка, но
 не затягивай с этим'''

THANK_FOR_FEEDBACK_MESSAGE = '''Спасибо за обратную связь. Мы это ценим!'''

EVENT_ACCEPTED_MESSAGE = '''Твоя заявка принята!'''

SORRY_EVENT_EXPIRED_MESSAGE = '''
Упс :( К сожалению, эта заявка была удалена.'''

YOU_LIKED_EVENT_MESSAGE = '''
Вот ссылочка человека, оставившего заявку -> vk.com/id{}. Пиши ему скорее!
'''

SEEN_EVENT_CHOICES = {
    'Мне нравится это предложение!': 1,
    'Покажи мне другое': 2,
    'Хочу оставить заявку': 3,
    'Хочу оставить фидбэк': 4
}

MAKE_SEEN_EVENT_CHOICES_MESSAGE = '\n'.join(
    ['{} - {}'.format(key, value) for key, value in SEEN_EVENT_CHOICES.items()]
)

SELECT_WHAT_TO_DO_CHOICES = {
    'Смотреть заявки других': 1,
    'Оставить заявку': 2,
    'Оставить фидбэк': 3
}

SELECT_WHAT_TO_DO_CHOICES_MESSAGE = 'Что будем делать?\n' + '\n'.join(
    ['{} - {}'.format(key, value)
     for key, value in SELECT_WHAT_TO_DO_CHOICES.items()]
)

CLEAN_UP_INTERVAL = 60 * 30  # in seconds
EVENT_DESCRIPTION_MAX_LENGTH = 300
EVENT_ATTACHMENTS_MAX_LENGTH = 400
N_OF_TIME_EVENT_REMAINS_ACTIVE = datetime.timedelta(
    days=4, hours=23, minutes=30
)
N_OF_TIME_EVENT_REMAINS_UNDELETED = datetime.timedelta(
    days=5
)
