from .regex import Regex


class Emoticons():
    def getEmoticons(self, inputString):
        """
          Emoticons are alphanumeric strings, no longer than 15 characters,
          contained in parenthesis.
          Eg: Hello (smiley)

          Method to parse input string and return a list of emoticons

          Params:
            inputString (str): the string to be parsed

          Return:
            A list of string of the emoticons in the inputString, if present
            An empty list if there are no emoticons in the inputString.
        """
        return Regex().emoticons().findall(inputString)
