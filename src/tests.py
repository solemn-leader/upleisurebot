from access_token import TOKEN
import vk_api
from helpers import get_random_id

API = vk_api.VkApi(token=TOKEN)

print(get_random_id())
