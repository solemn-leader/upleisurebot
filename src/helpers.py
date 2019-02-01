import random
from dateutil import parser
from datetime import date


def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])


def get_age_from_birth(bdate: str) -> int:
    from dateutil import parser
    born = parser.parse(bdate, dayfirst=True)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) <
                                     (born.month, born.day))
