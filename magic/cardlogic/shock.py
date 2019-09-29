from magic.card import Card
from magic.manacost import ManaCost

class Shock(Card):
    def __init__(self, id):
        super().__init__(id)
        self.name = "Shock"
        self.cardtypes["instant"] = True

    def __str__(self):
        return "Shock, " + str(self.id)

    def canplay(self, boardstate):
        # Check for normal conditions
        return super().canplay(boardstate)

    def shouldplay(self, boardstate):
        # Always just play if we can
        return True

    def manacost(self, boardstate):
        return ManaCost("r")

    def play(self, boardstate):
        boardstate.opponent_life -= 2
        return super().play(boardstate)
