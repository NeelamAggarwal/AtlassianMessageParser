from parser import create_app
import unittest
from parser.helper.emoticons import Emoticons

"""
	Unit test cases for testing Emoticons
"""


class EmoticonsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.emoticons = Emoticons()

    @classmethod
    def tearDownClass(cls):
        pass

    def assert_valid_emoticons(self, input, expectedValue):
        emoticonsList = self.emoticons.getEmoticons(input)
        self.assertEqual(len(emoticonsList), len(expectedValue))
        self.assertEqual(emoticonsList, expectedValue)

    def assert_invalid_emoticons(self, input):
        emoticonsList = self.emoticons.getEmoticons(input)
        self.assertEqual(len(emoticonsList), 0)

    def test_valid_emoticons(self):
        # One valid emoticon present
        self.assert_valid_emoticons('(smiley)', ['smiley'])

        # One valid emoticon present
        self.assert_valid_emoticons('(Hello(smiley))', ['smiley'])

        # One valid emoticon present
        self.assert_valid_emoticons('(Hello(smiley)Hello)', ['smiley'])

        # Two valid emoticons present
        self.assert_valid_emoticons('(smiley)(smiley)', ['smiley', 'smiley'])

        # One valid emoticons present, along with message.
        self.assert_valid_emoticons('Hello how are you? (smiley)', ['smiley'])

        # Emoticons with multiple brackets
        self.assert_valid_emoticons(
            'Hello how are you? (((smiley)))', ['smiley'])

        # One emoticon with symbols around the bracket
        self.assert_valid_emoticons('0=$$(smiley)$$', ['smiley'])

    def test_invalid_emoticons(self):
        # Empty string
        self.assert_invalid_emoticons('')

        # Empty brackets
        self.assert_invalid_emoticons('()')

        # Invalid emoticons, emoticons with non-alphanumeric value
        self.assert_invalid_emoticons('Hello (s====miley)')

        # Invalid emoticons, emoticons with non-alphanumeric value
        self.assert_invalid_emoticons('Hello (s_miley)')

        # Invalid emoticons length of emoticons great than 15
        self.assert_invalid_emoticons('Hello (thisisaverybigsmiley)')

        # No emoticons present
        self.assert_invalid_emoticons('Hello, how are you?')
