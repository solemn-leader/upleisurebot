import random
import unittest

import vk_api

from access_token import TOKEN
from consts import MY_ID

API = vk_api.VkApi(token=TOKEN)


class TestNothing(unittest.TestCase):
    def test_nothing(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
