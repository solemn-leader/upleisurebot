import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import access_token

API = vk_api.VkApi(token=access_token.TOKEN)


def write_msg(user_id, message):
    global API
    API.method(
        'messages.send', 
        {
            'user_id': user_id, 
            'message': message, 
            'random_id': get_random_id()
        }
    )


def main():
    global API
    longpoll = VkLongPoll(API)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "привет":
                    write_msg(event.user_id, "Хай")
                elif request == "пока":
                    write_msg(event.user_id, "Пока((")
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...", )
