from access_token import TOKEN
import vk_api
import unittest
from consts import MY_ID
import random

API = vk_api.VkApi(token=TOKEN)


class TestNothing(unittest.TestCase):
    def test_nothing(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
