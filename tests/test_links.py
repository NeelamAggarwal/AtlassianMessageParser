from parser.helper.links import Links
from bs4 import BeautifulSoup
import unittest
import urllib.request
from mock import patch, Mock, MagicMock

"""
    Unit test cases for testing Links
"""


class LinksTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.links = Links()

    @classmethod
    def tearDownClass(cls):
        pass

    @patch('parser.helper.links.urlopen')
    def test_links_with_links_in_message(self, mock_urlopen):
        """
            We are mocking urlopen to avoid making external requests from
            unit test cases.
        """
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '<html><title>Hello</title><html>'
        mock_urlopen.return_value = cm
        linksList = self.links.getLinks(
            'Hello, http://www.google.com and https://www.yahoo.com')

        self.assertEqual(len(linksList), 2)
        self.assertEqual(linksList[0]['url'], 'http://www.google.com')
        self.assertEqual(linksList[0]['title'], 'Hello')
        self.assertEqual(linksList[1]['url'], 'https://www.yahoo.com')
        self.assertEqual(linksList[1]['title'], 'Hello')

    @patch('parser.helper.links.urlopen')
    def test_links_with_no_links_in_message(self, mock_urlopen):
        """
            We are mocking urlopen to avoid making external requests from
            unit test cases.
        """
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '<html><title>Hello</title><html>'
        mock_urlopen.return_value = cm

        linksList = self.links.getLinks('Hello, how are you?')
        self.assertEqual(len(linksList), 0)

    @patch('parser.helper.links.urlopen')
    def test_links_with_invalid_link_in_message(self, mock_urlopen):
        """
            We are mocking urlopen to avoid making external requests from
            unit test cases.
        """
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '<html><title>Hello</title><html>'
        mock_urlopen.return_value = cm

        linksList = self.links.getLinks(
            'Hello, wwww.google.com 423.google.com how are you?')
        self.assertEqual(len(linksList), 0)
