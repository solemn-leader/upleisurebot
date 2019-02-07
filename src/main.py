from vk_api.longpoll import VkLongPoll, VkEventType
from bot import make_bot_response, API
import os
from models import create_tables
from backg_tasks import DBCleanUp
from consts import CLEAN_UP_INTERVAL


def main():
    longpoll = VkLongPoll(API)
    create_tables()
    clean_up = DBCleanUp(CLEAN_UP_INTERVAL)
    print("STARTED")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                make_bot_response(event)


if __name__ == "__main__":
    main()
