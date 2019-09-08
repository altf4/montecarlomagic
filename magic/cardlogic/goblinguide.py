from magic.card import Card
from magic.manacost import ManaCost

class GoblinGuide(Card):
    def __init__(self, id):
        super().__init__(id)
        self.power = 2
        self.iscreature = True
        self.priority = 200

    def __str__(self):
        return "Goblin Guide, " + str(self.id)

    def canplay(self, boardstate):
        # Check for normal conditions
        return super().canplay(boardstate)

    def shouldplay(self, boardstate):
        # Always just play if we can
        return True

    def manacost(self, boardstate):
        return ManaCost("r")

    def play(self, boardstate):
        self.summoning_sick = False
        return super().play(boardstate)
