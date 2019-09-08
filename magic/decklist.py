from magic.card import Card
import copy

import magic.cardlogic


class Decklist():
    """A decklist.
    """

    def __init__(self, filename="decklist.txt"):
        """Read decklist from txt file
        """
        with open(filename) as f:
            self.lines = f.readlines()
            self.lines = [x.strip() for x in self.lines]
            self._parse_decklist(self.lines)

    def _parse_decklist(self, decklist_strings):
        """ Parses a list of decklist strings into objects
        """
        self.deck = []
        id = 1
        for line in decklist_strings:
            # Parse out the quantity prefix
            for _ in range(int(line.split(" ", 1)[0])):
                cardname = (line.split(" ", 1)[1]).replace(" ", "")
                card = getattr(magic.cardlogic, cardname)(id)
                id += 1
                self.deck.append(card)

    def __len__(self):
        return len(self.deck)

    def get_library(self):
        """Get a sample shuffled library from the decklist
        """
        self._parse_decklist(self.lines)
        return self.deck
