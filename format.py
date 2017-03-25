#!/usr/bin/python3.6
# -*-coding:Utf-8 -*


class Color:
    """Class used the color console text"""
    colors = {'PINK': '\033[95m', 'BLUE': '\033[94m', 'GREEN': '\033[92m', 'YELLOW': '\033[93m',
                   'RED': '\033[91m', 'ENDC': '\033[0m', 'BOLD': '\033[1m', 'UNDERLINE': '\033[4m'}

    def __init__(self, text, color, colors=colors):
        """This class contain :
- colors : the list of colors with 'name':'code'
- text : the text to display
- color : the chosen color"""

        self.color = colors[color]

        self.text = str(text)

    def __repr__(self):
        """Return the formated text and 'ENDC' at the end"""
        return self.color + self.text + self.colors['ENDC']

    def __len__(self):
        """Return the true length of the 'str' object to "try" to avoid formatting error"""
        return len(self.text)

