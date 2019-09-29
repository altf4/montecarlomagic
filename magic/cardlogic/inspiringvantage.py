from magic.card import Card
from magic.manacost import ManaCost

class InspiringVantage(Card):
    def __init__(self, id):
        super().__init__(id)
        self.cardtypes["land"] = True
        self.id = id
        self.tapsfor["red"] = True
        self.tapsfor["white"] = True
        self.priority = 101
        self.name = "Inspiring Vantage"

    def __str__(self):
        return "Inspiring Vantage, " + str(self.id)

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
        # Fastland
        if len(boardstate.lands) > 3:
            self.istapped = True
