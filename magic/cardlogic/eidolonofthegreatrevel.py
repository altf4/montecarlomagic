from magic.card import Card
from magic.manacost import ManaCost

class EidolonOfTheGreatRevel(Card):
    def __init__(self, id):
        super().__init__(id)
        self.power = 2
        self.cardtypes["creature"] = True
        self.priority = 180
        self.name = "Eidolon Of The Great Revel"

    def __str__(self):
        return "Eidolon Of The Great Revel, " + str(self.id)

    def canplay(self, boardstate):
        # Check for normal conditions
        return super().canplay(boardstate)

    def shouldplay(self, boardstate):
        # Always just play if we can
        return True

    def manacost(self, boardstate):
        return ManaCost("rr")

    def play(self, boardstate):
        return super().play(boardstate)
