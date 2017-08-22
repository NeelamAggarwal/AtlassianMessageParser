import re


class Regex:
    def _regex(function):
        def wrapper(self):
            regex = function(self)
            return re.compile(regex)
        return wrapper

    @_regex
    def mentions(self):
        """
        Regex to parse the mentions. Eg: Hello @atlassian
        ( 			start the group
        ?: 			do not capture this group
        ^|\W 		search at startpoint OR for non-word character
        ) 			end of group
        (			start of group
        ?:			do not capture this group
        \			escapes special character which will be @
        @			search for '@'
        )			end of group
        (			start of capturing group
        \w 			search for word character
        +			search for one or more word character
        )			end of capturing group
        """
        regex = r'(?:^|\W)(?:\@)(\w+)'
        return regex

    @_regex
    def links(self):
        """
        Regex to parse the links. Eg: Hello http://www.google.com
        http		search for 'http' in the string
        [s]? 		search for one 's' optional
        ://www. 	search for one or more non space character
        [a-zA-Z0-9]+		search for alphanumeric one or more characters
        . 			search for '.' character
        [a-zA-Z]	search for alpha one or more characters
        """
        regex = r"http[s]?://www.[a-zA-Z0-9]+.[a-zA-Z]+"  # This may not include all testcases
        return regex

    @_regex
    def emoticons(self):
        """
        Regex to parse the emoticons. Eg: Hello (smiley)
        \		escapes the special character which will be (
        (		search for character '('
        (		start capturing group
        [a-zA-Z0-9] 		search match for alpahnumeric character
        {1,15}	search for minimum of 1 length and maximum of 15 length word character
        )		end of capturing group
        \		escapes the special character which will be )
        ) 		search for character ')'
        """
        regex = r'\(([a-zA-Z0-9]{1,15})\)'
        return regex
