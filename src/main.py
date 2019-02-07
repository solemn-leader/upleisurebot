from vk_api.longpoll import VkLongPoll, VkEventType
from bot import make_bot_response, API
import os
from models import create_tables
from backg_tasks import *


def main():
    longpoll = VkLongPoll(API)
    clean_up = DBCleanUp()
    create_tables()
    print("STARTED")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                make_bot_response(event)


if __name__ == "__main__":
    main()
