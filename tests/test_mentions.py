from parser import create_app
import unittest
from parser.helper.mentions import Mentions

"""
	Unit test cases for testing Mentions
"""


class MentionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mentions = Mentions()

    @classmethod
    def tearDownClass(cls):
        pass

    def assert_valid_mentions(self, input, expectedValue):
        mentionsList = self.mentions.getMentions(input)
        self.assertEqual(len(mentionsList), len(expectedValue))
        self.assertEqual(mentionsList, expectedValue)

    def assert_invalid_mentions(self, input):
        mentionsList = self.mentions.getMentions(input)
        self.assertEqual(len(mentionsList), 0)

    def test_valid_mentions(self):
        # One valid mention present
        self.assert_valid_mentions('@atlassian', ['atlassian'])

        # One valid mention present along with message
        self.assert_valid_mentions(
            'Hello @atlassian, how are you?', ['atlassian'])

        # Two valid mention present along with message
        self.assert_valid_mentions(
            'Hello @atlassian and @bob, how are you?', [
                'atlassian', 'bob'])

        # When we dont have space in from of atlassian
        self.assert_valid_mentions('hello@atlassian.com and @bob.', ['bob'])

        # When we have symbols in front of Mentions
        self.assert_valid_mentions('$#@bob', ['bob'])

        # When we have symbol at the end of Mention
        self.assert_valid_mentions('Hello @bob$$$', ['bob'])

        # Mentions with symbol
        self.assert_valid_mentions('@atlass_ian', ['atlass_ian'])

        # Mentions inside a bracket
        self.assert_valid_mentions('@bob', ['bob'])

    def test_invalid_mentions(self):
        # When there are no Mentions
        self.assert_invalid_mentions('Hello, how are you?')

        # Emtpy string
        self.assert_invalid_mentions('')

        # Invalid mentions, eg email
        self.assert_invalid_mentions('user@atlassian.com')

        # Emtpy bracket
        self.assert_invalid_mentions('()')
