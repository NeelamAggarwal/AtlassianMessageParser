from .regex import Regex
from bs4 import BeautifulSoup
from urllib.request import urlopen


class Links():
    def getTitle(self, link):
        """
          Method to fetch a title for the passed link

          Params:
            link (str): the url to fetch title for

          Return:
            Title of the webpage if link is valid, otherwise returns None
        """
        try:
            soup = BeautifulSoup(urlopen(link), "html.parser")
            return soup.title.string
        except Exception as e:
            return None

    def getLinks(self, inputString):
        """
          Parses URLs.
          Method to parse input string and return a array of link and title.

          Params:
            inputString (str): the string to be parsed

          Return:
            A list of links and title, if there are links in the inputString
            An empty list if there are no links in the inputString.
        """
        links = Regex().links().findall(inputString)
        outputLinks = []
        for link in links:
            outputLinks.append({'url': link, 'title': self.getTitle(link)})
        return outputLinks
