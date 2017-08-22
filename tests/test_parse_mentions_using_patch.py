import json
from parser import create_app
import unittest
from injector import inject, singleton
from parser.helper.mentions import Mentions
from parser.helper.emoticons import Emoticons
from parser.helper.links import Links
from mock import patch, Mock, MagicMock

"""
	Unit test cases for endpoint /api/v1/parse-message.
	We are using @patch to intercept urlopen call and
	returning a default value.
"""


class ParseMessageIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app(config_name='testing')
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_missing_parameter(self):
        rv = self.client.get('/api/v1/parse-message')
        self.assertEquals(rv.status_code, 422)

    def test_valid_mentions(self):
        # One valid mention present
        self.assert_valid_input('@atlassian', ['atlassian'], 'mentions')

        # One valid mention present along with message
        self.assert_valid_input(
            'Hello @atlassian, how are you?',
            ['atlassian'],
            'mentions')

        # Two valid mention present along with message
        self.assert_valid_input(
            'Hello @atlassian and @bob, how are you?', [
                'atlassian', 'bob'], 'mentions')

        # When we dont have space in from of atlassian
        self.assert_valid_input(
            'hello@atlassian.com and @bob.',
            ['bob'],
            'mentions')

        # When we have symbols in front of Mentions
        self.assert_valid_input('$#@bob', ['bob'], 'mentions')

        # When we have symbol at the end of Mention
        self.assert_valid_input('Hello @bob$$$', ['bob'], 'mentions')

        # Mentions with symbol
        self.assert_valid_input('@atlass_ian', ['atlass_ian'], 'mentions')

        # Mentions inside a bracket
        self.assert_valid_input('@bob', ['bob'], 'mentions')

    def test_invalid_emoticons(self):
        # Empty string
        self.assert_invalid_emoticons('', 'mentions')

        # Empty brackets
        self.assert_invalid_emoticons('()', 'mentions')

        # Invalid emoticons, emoticons with non-alphanumeric value
        self.assert_invalid_emoticons('Hello (s====miley)', 'mentions')

        # Invalid emoticons, emoticons with non-alphanumeric value
        self.assert_invalid_emoticons('Hello (s_miley)', 'mentions')

        # Invalid emoticons length of emoticons great than 15
        self.assert_invalid_emoticons(
            'Hello (thisisaverybigsmiley)', 'mentions')

        # No emoticons present
        self.assert_invalid_emoticons('Hello, how are you?', 'mentions')

    def test_valid_emoticons(self):
        # One valid emoticons
        self.assert_valid_input('(smiley)', ['smiley'], 'emoticons')

        # One valid emoticon present
        self.assert_valid_input('(Hello(smiley))', ['smiley'], 'emoticons')

        # One valid emoticon present
        self.assert_valid_input(
            '(Hello(smiley)Hello)',
            ['smiley'],
            'emoticons')

        # Two valid emoticons present
        self.assert_valid_input(
            '(smiley)(smiley)', [
                'smiley', 'smiley'], 'emoticons')

        # One valid emoticons present, along with message.
        self.assert_valid_input(
            'Hello how are you? (smiley)',
            ['smiley'],
            'emoticons')

        # Emoticons with multiple brackets
        self.assert_valid_input(
            'Hello how are you? (((smiley)))',
            ['smiley'],
            'emoticons')

        # One emoticon with symbols around the bracket
        self.assert_valid_input('0=$$(smiley)$$', ['smiley'], 'emoticons')

    def test_invalid_emoticons(self):
        # Empty string
        self.assert_invalid_input('', 'emoticons')

        # Empty brackets
        self.assert_invalid_input('()', 'emoticons')

        # Invalid emoticons, emoticons with non-alphanumeric value
        self.assert_invalid_input('Hello (s====miley)', 'emoticons')

        # Invalid emoticons, emoticons with non-alphanumeric value
        self.assert_invalid_input('Hello (s_miley)', 'emoticons')

        # Invalid emoticons length of emoticons great than 15
        self.assert_invalid_input('Hello (thisisaverybigsmiley)', 'emoticons')

        # No emoticons present
        self.assert_invalid_input('Hello, how are you?', 'emoticons')

    @patch('parser.helper.links.urlopen')
    def test_links_with_links_in_message(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '<html><title>Hello</title><html>'
        mock_urlopen.return_value = cm

        rv = self.client.get(
            '/api/v1/parse-message?input=Hello, http://www.google.com and https://www.yahoo.com')
        self.assertEquals(rv.status_code, 200)
        resp = json.loads(rv.get_data(as_text=True))
        self.assertEquals(len(resp['links']), 2)
        self.assertEquals(str(resp['links'][0]['url']),
                          'http://www.google.com')
        self.assertEquals(str(resp['links'][0]['title']), 'Hello')
        self.assertEquals(str(resp['links'][1]['url']),
                          'https://www.yahoo.com')
        self.assertEquals(str(resp['links'][1]['title']), 'Hello')

    @patch('parser.helper.links.urlopen')
    def test_links_with_no_links_in_message(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '<html><title>Hello</title><html>'
        mock_urlopen.return_value = cm

        rv = self.client.get('/api/v1/parse-message?input=Hello, how are you?')
        self.assertEquals(rv.status_code, 200)
        resp = json.loads(rv.get_data(as_text=True))
        self.assertEquals('links' in resp, False)

    @patch('parser.helper.links.urlopen')
    def test_links_with_invalid_link_in_message(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '<html><title>Hello</title><html>'
        mock_urlopen.return_value = cm

        rv = self.client.get(
            '/api/v1/parse-message?input=Hello, wwww.google.com 423.google.com how are you?')
        self.assertEquals(rv.status_code, 200)
        resp = json.loads(rv.get_data(as_text=True))
        self.assertEquals('links' in resp, False)

    @patch('parser.helper.links.urlopen')
    def test_get_parse_response(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '<html><title>Hello</title><html>'
        mock_urlopen.return_value = cm

        response = self.client.get(
            '/api/v1/parse-message?input=Hello @atlassian (smiley) http://www.atlassian.com')
        self.assertEqual(response.status_code, 200)
        responseBody = json.loads(response.get_data(as_text=True))
        self.assertEquals(responseBody['mentions'], ['atlassian'])
        self.assertEquals(responseBody['emoticons'], ['smiley'])
        self.assertEquals(
            responseBody['links'][0]['url'],
            'http://www.atlassian.com')

    def assert_valid_input(self, emoticons, expectedValue, responseKey):
        rv = self.client.get('/api/v1/parse-message?input=' + emoticons)
        self.assertEquals(rv.status_code, 200)
        resp = json.loads(rv.get_data(as_text=True))
        self.assertEquals(len(resp[responseKey]), len(expectedValue))
        self.assertEquals(resp[responseKey], expectedValue)

    def assert_invalid_input(self, emoticons, responseKey):
        rv = self.client.get('/api/v1/parse-message?input=' + emoticons)
        self.assertEquals(rv.status_code, 200)
        resp = json.loads(rv.get_data(as_text=True))
        self.assertEquals(responseKey in resp, False)
