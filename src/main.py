from vk_api.longpoll import VkLongPoll, VkEventType
from helpers import make_bot_response, API
import os


def main():
    longpoll = VkLongPoll(API)
    print("STARTED")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                make_bot_response(event)


if __name__ == "__main__":
    main()
