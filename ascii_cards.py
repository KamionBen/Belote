from format import Color

class Card(object):

    card_values = {
        'As': [11,11],  # [pas atout, atout]
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': [0,0],
        '8': [0,0],
        '9': [0,14],
        '10': [10,10],
        'Valet': [2,20],
        'Dame': [3,3],
        'Roi': [4,4]
    }

    ordre = {'As': 8,
             '7': 1,
             '8': 2,
             '9': 3,
             '10': 7,
             'Valet': 4,
             'Dame': 5,
             'Roi': 6}

    ordre_atout = {'As': 14,
             '7': 9,
             '8': 10,
             '9': 15,
             '10': 13,
             'Valet': 16,
             'Dame': 11,
             'Roi': 12}

    def __init__(self, couleur, valeur):
        """
        :param couleur: The face of the card, e.g. Spade or Diamond
        :param valeur: The value of the card, e.g 3 or King
        """
        self.couleur = couleur.capitalize()
        self.valeur = valeur
        self.points = self.card_values[valeur]
        self.ordre = self.ordre[valeur]
        self.ordre_atout = self.ordre_atout[valeur]

    def __repr__(self):
        return "{} de {}".format(self.valeur, self.couleur)

    def get_ordre(self, atout):
        if self.couleur == atout:
            return self.ordre_atout
        else:
            return self.ordre

    def get_points(self, atout):
        if atout == self.couleur:
            return self.points[1]
        else:
            return self.points[0]


def ascii_version_of_card(*cards, return_string=True, atout=''):
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :param return_string: By default we return the string version of the card, but the dealer hide the 1st card and we
    keep it as a list so that the dealer can add a hidden card in front of the list
    """
    # we will use this to prints the appropriate icons for each card
    suits_name = ['Pique', 'Carreau', 'Coeur', 'Trèfle']
    suits_symbols = ['♠', '♦', '♥', '♣']

    # create an empty list of list, each sublist is a line
    lines = [[] for i in range(7)]

    for index, card in enumerate(cards):
        # "King" should be "K" and "10" should still be "10"
        if card.valeur == '10':  # ten is the only one who's valeur is 2 char long
            rank = card.valeur
            space = ''  # if we write "10" on the card that line will be 1 char to long
        else:
            rank = card.valeur[0]  # some have a valeur of 'King' this changes that to a simple 'K' ("King" doesn't fit)
            space = ' '  # no "10", we use a blank space to will the void
        # get the cards couleur in two steps
        couleur = suits_name.index(card.couleur)
        suit = suits_symbols[couleur]

        if suit in ['♦', '♥']:
            rank = Color(rank, 'RED')
            suit = Color(suit, 'RED')

        if atout == suits_name[couleur]:
            # add the individual card on a line by line basis
            lines[0].append(str(Color('┌───────┐','YELLOW')))
            lines[1].append(str(Color('│','YELLOW'))+'{}{}     '.format(rank, space)+str(Color('│','YELLOW'))) # use two {} one for char, one for space or char
            lines[2].append(str(Color('│       │','YELLOW')))
            lines[3].append(str(Color('│   ','YELLOW'))+'{}   '.format(suit)+str(Color('│', 'YELLOW')))
            lines[4].append(str(Color('│       │','YELLOW')))
            lines[5].append(str(Color('│     ','YELLOW')) + '{}{}'.format(space, rank)+str(Color('│', 'YELLOW')))
            lines[6].append(str(Color('└───────┘','YELLOW')))
        else:
            # add the individual card on a line by line basis
            lines[0].append('┌───────┐')
            lines[1].append('│{}{}     │'.format(rank, space))  # use two {} one for char, one for space or char
            lines[2].append('│       │')
            lines[3].append('│   {}   │'.format(suit))
            lines[4].append('│       │')
            lines[5].append('│     {}{}│'.format(space, rank))
            lines[6].append('└───────┘')
    result = []
    for index, line in enumerate(lines):
        result.append(''.join(lines[index]))

    # hidden cards do not use string
    if return_string:
        return '\n'.join(result)
    else:
        return result


def ascii_version_of_hidden_card(*cards):
    """
    Essentially the dealers method of print ascii cards. This method hides the first card, shows it flipped over
    :param cards: A list of card objects, the first will be hidden
    :return: A string, the nice ascii version of cards
    """
    # a flipper over card. # This is a list of lists instead of a list of string becuase appending to a list is better then adding a string
    lines = [['┌───────┐'], ['│░░░░░░░│'], ['│░░░░░░░│'], ['│░░░░░░░│'], ['│░░░░░░░│'], ['│░░░░░░░│'], ['└───────┘']]

    # store the non-flipped over card after the one that is flipped over
    cards_except_first = ascii_version_of_card(*cards[1:], return_string=False)
    for index, line in enumerate(cards_except_first):
        lines[index].append(line)

    # make each line into a single list
    for index, line in enumerate(lines):
        lines[index] = ''.join(line)

    # convert the list into a single string
    return '\n'.join(lines)


# TEST CASES

if __name__ == '__main__':
    test_card_1 = Card('Diamonds', '4')
    test_card_2 = Card('Clubs', 'Ace')
    test_card_3 = Card('Spades', 'Jack')
    test_card_4 = Card('Hearts', '10')

    print(ascii_version_of_card(test_card_1, test_card_2, test_card_3, test_card_4))
    print(ascii_version_of_hidden_card(test_card_1, test_card_2, test_card_3, test_card_4))
    # print(ascii_version_of_hidden_card(test_card_1, test_card_2))