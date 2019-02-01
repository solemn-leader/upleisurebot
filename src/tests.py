from access_token import TOKEN
import vk_api
from helpers import get_age_from_birth

API = vk_api.VkApi(token=TOKEN)
# print(
#     API.method(
#         'users.get',
#         {
#             'user_ids': '262057646',
#             'fields': 'city, bdate'
#         }
#     )
# )

print(get_age_from_birth('1.1.2000'))
