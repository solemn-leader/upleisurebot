import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from access_token import TOKEN
from helpers import *

API = vk_api.VkApi(token=TOKEN)


def main():
    global API
    longpoll = VkLongPoll(API)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                write_msg(API, event.user_id, "Не поняла вашего ответа...", )


if __name__ == "__main__":
    main()
