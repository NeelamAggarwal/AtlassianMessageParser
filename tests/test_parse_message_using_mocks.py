import json
from parser import create_app
import unittest
from injector import inject, singleton
from parser.helper.mentions import Mentions
from parser.helper.emoticons import Emoticons
from parser.helper.links import Links
from mock import MagicMock

"""
	Unit test cases for endpoint /api/v1/parse-message.
	We are using mock for Mentions, Emoticons and
	Links
"""


class ParseMessageTest(unittest.TestCase):
    @classmethod
    def configureTesting(self, binder):
        mentions = Mentions()
        mentions.getMentions = MagicMock(return_value=['atlassian'])

        emoticons = Emoticons()
        emoticons.getEmoticons = MagicMock(return_value=['smiley'])

        links = Links()
        linkResponse = {}
        linkResponse['url'] = 'http://wwww.atlassian.com'
        linkResponse['title'] = 'Hello'
        links.getLinks = MagicMock(return_value=[linkResponse])
        binder.bind(
            Mentions,
            to=mentions,
            scope=singleton,)
        binder.bind(
            Emoticons,
            to=emoticons,
            scope=singleton,)
        binder.bind(
            Links,
            to=links,
            scope=singleton,)

    @classmethod
    def setUpClass(cls):
        app = create_app(configure=cls.configureTesting, config_name='testing')
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_parse_response(self):
        response = self.client.get(
            '/api/v1/parse-message?input=Hello @atlassian (atlassian) http://wwww.atlassian.com')
        self.assertEqual(response.status_code, 200)
        responseBody = json.loads(response.get_data(as_text=True))
        self.assertEquals(responseBody['mentions'], ['atlassian'])
        self.assertEquals(responseBody['emoticons'], ['smiley'])
        self.assertEquals(
            responseBody['links'][0]['url'],
            'http://wwww.atlassian.com')

    def test_get_parse_response_missing_input_return_unprocessable_entity(
            self):
        response = self.client.get('/api/v1/parse-message')
        self.assertEqual(response.status_code, 422)
        responseBody = json.loads(response.get_data(as_text=True))
        self.assertEquals(
            responseBody['messages']['input'],
            ['Missing data for required field.'])
