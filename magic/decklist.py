from magic.card import Card
import magic.cardlogic

from random import sample


class Decklist():
    """A decklist.
    """

    def __init__(self, filename="decklist.txt"):
        """Read decklist from txt file
        """
        with open(filename) as f:
            self.lines = f.readlines()
            self.lines = [x.strip() for x in self.lines]
            # A dictionary indexing on card ID
            self.decklist = {}
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
                self.decklist[id] = card
                id += 1
                self.deck.append(card)

    def __len__(self):
        return len(self.deck)

    def get_library(self):
        """Get a sample library from the decklist
        """
        # self._parse_decklist(self.lines)
        return list(self.deck)

    def sample_hand(self, count):
        """Get a random sample hand of 'count' card IDs
        """
        return sample(range(1, len(self)+1), count)

    def cardstring(self, id):
        """Get a printable string of a card from the given ID
        """
        return str(self.decklist[id])
