from .regex import Regex


class Mentions():
    def getMentions(self, inputString):
        """
          Mentions always starts with an '@' and ends when hitting a non-word character.
          Eg: Hello @atlassian

          Method to parse input string and return a list of mentions

          Params:
            inputString (str): the string to be parsed

          Return:
            A list of string of the mentions in the inputString, if present
            An empty list if there are no mentions in the inputString.
        """
        return Regex().mentions().findall(inputString)
