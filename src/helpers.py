import random
from dateutil import parser
from datetime import date, datetime
from models import User, TeenEvent, YoungEvent
from consts import (
    AgeGroups,
    N_OF_TIME_EVENT_REMAINS_ACTIVE,
    SORRY_EVENT_EXPIRED_MESSAGE,
    YOU_LIKED_EVENT_MESSAGE,
    NO_EVENTS_MESSAGE
)
from dateutil import parser


def get_random_id() -> str:
    # random id for message
    return random.getrandbits(31) * random.choice([-1, 1])


def get_age_from_birth(bdate: str) -> int:
    '''gets birthday date %d.%m.%y and returns age in years'''
    born = parser.parse(bdate, dayfirst=True)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) <
                                     (born.month, born.day))


def get_event_for_user(user_id) -> (str, str):
    '''returns message and attachments, NO_EVENT_MESSAGE if necessary'''
    if User.select().where(User.user_id == user_id).exists():
        user = User.get(User.user_id == user_id)
        age_group, last_seen_event_pk = user.age_group, user.last_seen_event_pk
    else:  # user does not exist
        return (NO_EVENTS_MESSAGE, '')

    if age_group == AgeGroups.TEENS:
        event_class = TeenEvent
    else:
        event_class = YoungEvent
    # we find the closest event which user has not seen
    # and which is still active
    event = event_class.get_or_none(
        (event_class.owner != user) &  # not left by this user
        (event_class.pk > last_seen_event_pk) &  # not seen by this user
        (event_class.time_published  # still active
            > (datetime.utcnow() - N_OF_TIME_EVENT_REMAINS_ACTIVE)) &
        (event_class.city == user.city)  # takes place in user's city
        )
    if event:  # we find such event
        User.update(last_seen_event_pk=event.pk).where(User.user_id == user_id)
        return (event.description, event.attachments)
    else:  # no events to show
        return (NO_EVENTS_MESSAGE, '')


def user_liked_event_get_response(user_id) -> (str, str):
    user = User.get_or_none(User.user_id == user_id)
    if not user:  # smth went wrong
        return (SORRY_EVENT_EXPIRED_MESSAGE, '')

    event_pk, age_group = user.last_seen_event_pk, user.age_group
    if age_group == AgeGroups.TEENS:
        event_class = TeenEvent

    else:
        event_class = YoungEvent

    event = event_class.get_or_none(event_class.pk == event_pk)

    if not event:  # event user liked has expired
        return (SORRY_EVENT_EXPIRED_MESSAGE, '')

    else:
        return (YOU_LIKED_EVENT_MESSAGE.format(event.owner.user_id), '')
