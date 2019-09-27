from magic.card import Card
from magic.manacost import ManaCost

class SunbakedCanyon(Card):
    def __init__(self, id):
        super().__init__(id)
        self.land = True
        self.id = id
        self.tapsfor["red"] = True
        self.tapsfor["white"] = True
        self.priority = 100
        self.name = "Sunbaked Canyon"

    def __str__(self):
        return "Sunbaked Canyon, " + str(self.id)

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
