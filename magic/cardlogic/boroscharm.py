from magic.card import Card
from magic.manacost import ManaCost

class BorosCharm(Card):
    def __init__(self, id):
        super().__init__(id)

    def __str__(self):
        return "Boros Charm, " + str(self.id)

    def canplay(self, boardstate):
        # Check for normal conditions
        return super().canplay(boardstate)

    def shouldplay(self, boardstate):
        # Always just play if we can
        return True

    def manacost(self, boardstate):
        return ManaCost("wr")

    def play(self, boardstate):
        boardstate.opponent_life -= 4
        return super().play(boardstate)
