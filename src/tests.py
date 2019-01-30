from access_token import TOKEN
import vk_api

API = vk_api.VkApi(token=TOKEN)
print(
    API.method(
        'users.get',
        {
            'user_ids': '210045485'
        }
    )
)
