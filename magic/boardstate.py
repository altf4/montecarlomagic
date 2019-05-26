from random import shuffle

class Boardstate():
    library = []
    graveyard = []
    battlefield = []
    hand = []
    lands = []

    # Dict of flags (default false) affecting the gamestate this turn
    thisturn = {}

    def __init__(self, decklist):
        self.decklist = decklist
        self.library = self.decklist.get_library()
        shuffle(self.library)

    def scoop(self):
        """Reset the gamestate to all cards in library
        """
        self.library = self.decklist.get_library()
        shuffle(self.library)
        self.graveyard = []
        self.battlefield = []
        self.hand = []
        self.lands = []
        self.untap()

    def draw(self, amount=1):
        if amount > len(self.library):
            return False
        for i in range(amount):
            self.hand.append(self.library[0])
            del [self.library[0]]
        return True

    def untap(self):
        # Reset "end of turn" flags
        self.thisturn = dict.fromkeys(self.thisturn, False)

        for card in self.lands:
            card.istapped = False
        for card in self.battlefield:
            card.istapped = False

    def cleanup(self):
        # TODO: Discard to hand size
        pass
