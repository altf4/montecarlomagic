from magic.card import Card
from magic.manacost import ManaCost

class Mountain(Card):
    def __init__(self, id):
        super().__init__(id)
        self.land = True
        self.id = id
        self.tapsfor["red"] = True
        self.priority = 99
        self.fetchable = True
        self.name = "Mountain"

    def __str__(self):
        return "Mountain, " + str(self.id)

    def canplay(self, boardstate):
        # Check for normal conditions
        return super().canplay(boardstate)

    def shouldplay(self, boardstate):
        # Always just play if we can
        return True

    def manacost(self, boardstate):
        return ManaCost("0")

    def play(self, boardstate):
        return super().play(boardstate)
