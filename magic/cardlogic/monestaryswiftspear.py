from magic.card import Card
from magic.manacost import ManaCost

class MonestarySwiftspear(Card):
    def __init__(self, id):
        super().__init__(id)
        self.power = 1
        self.cardtypes["creature"] = True
        self.priority = 195
        self.name = "Monestary Swiftspear"
        self.cardtypes["creature"] = True
        self.keywords["haste"] = True
        self.keywords["prowess"] = True

    def __str__(self):
        return "Monestary Swiftspear, " + str(self.id)

    def canplay(self, boardstate):
        # Check for normal conditions
        return super().canplay(boardstate)

    def shouldplay(self, boardstate):
        # Always just play if we can
        return True

    def manacost(self, boardstate):
        return ManaCost("r")

    def play(self, boardstate):
        return super().play(boardstate)
