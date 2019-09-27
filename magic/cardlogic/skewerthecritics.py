from magic.card import Card
from magic.manacost import ManaCost

class SkewerTheCritics(Card):
    def __init__(self, id):
        super().__init__(id)
        self.priority = 220
        self.name = "Skewer The Critics"

    def __str__(self):
        return "Skewer The Critics, " + str(self.id)

    def canplay(self, boardstate):
        # Check for normal conditions
        return super().canplay(boardstate)

    def shouldplay(self, boardstate):
        # Always just play if we can
        return True

    def manacost(self, boardstate):
        if boardstate.opponent_life < boardstate.opponent_life_start_turn:
            return ManaCost("r")
        else:
            return ManaCost("2r")

    def play(self, boardstate):
        boardstate.opponent_life -= 3
        return super().play(boardstate)
