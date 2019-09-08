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
            self.deck = []
            lines = f.readlines()
            lines = [x.strip() for x in lines]
            id = 1
            for line in lines:
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
        return copy.deepcopy(self.deck)
