import random
from dateutil import parser
from datetime import date, datetime
from models import User, TeenEvent, YoungEvent
from consts import (
    AgeGroups,
    N_OF_TIME_EVENT_REMAINS_ACTIVE,
    SORRY_EVENT_EXPIRED_MESSAGE,
    YOU_LIKED_EVENT_MESSAGE
)
from peewee import fn


def get_random_id() -> str:
    return random.getrandbits(31) * random.choice([-1, 1])


def get_age_from_birth(bdate: str) -> int:
    from dateutil import parser
    born = parser.parse(bdate, dayfirst=True)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) <
                                     (born.month, born.day))


def get_event_for_user(user_id) -> (str, str):
    '''returns message and attachments'''
    if User.select().where(User.user_id == user_id).exists():
        user = User.get(User.user_id == user_id)
        age_group, last_seen_event_pk = user.age_group, user.last_seen_event_pk
    else:  # user does not exist
        return ('', '')

    if age_group == AgeGroups.TEENS:
        event_class = TeenEvent
    else:
        event_class = YoungEvent
    # we must choose the max event_pk user has seen
    event = event_class.get_or_none(
        event_class.pk > last_seen_event_pk,
        event_class.time_published +
        N_OF_TIME_EVENT_REMAINS_ACTIVE < datetime.utcnow(),
        event_class.owner != user)
    if event:
        User.update(last_seen_event_pk=event.pk).where(User.user_id == user_id)
        return (event.description, event.attachments)
    else:  # no events to show
        return ('', '')


def user_liked_event_get_response(user_id) -> (str, str):
    user = User.get_or_none(User.user_id == user_id)
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
