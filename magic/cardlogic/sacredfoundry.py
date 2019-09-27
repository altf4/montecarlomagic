from magic.card import Card
from magic.manacost import ManaCost

class SacredFoundry(Card):
    def __init__(self, id):
        super().__init__(id)
        self.land = True
        self.id = id
        self.tapsfor["red"] = True
        self.tapsfor["white"] = True
        self.priority = 101
        self.fetchable = True
        self.name = "Sacred Foundry"

    def __str__(self):
        return "Sacred Foundry, " + str(self.id)

    def canplay(self, boardstate):
        # Check for normal conditions
        return super().canplay(boardstate)

    def shouldplay(self, boardstate):
        # Always just play if we can
        return True

    def manacost(self, boardstate):
        return ManaCost("0")

    def play(self, boardstate):
        super().play(boardstate)
