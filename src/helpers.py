import random
from dateutil import parser
from datetime import date
from models import User, Event


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
    return
