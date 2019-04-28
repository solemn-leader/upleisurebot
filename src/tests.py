import random
import unittest

import vk_api

from access_token import TOKEN
from consts import MY_ID
from bot import everyone_allowed

API = vk_api.VkApi(token=TOKEN)


class TestNothing(unittest.TestCase):
    def test_nothing(self):
        self.assertEqual(True, True)


class TestWhoIsAllowed(unittest.TestCase):
    def test_everyone_allowed(self):
        self.assertTrue(everyone_allowed([1]))

    def test_noone_allowed(self):
        self.assertFalse(everyone_allowed([]))


if __name__ == '__main__':
    unittest.main()
