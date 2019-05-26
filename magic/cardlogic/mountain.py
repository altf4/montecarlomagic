from magic.card import Card

class Mountain(Card):
    def __init__(self, id):
        super().__init__(id)
        self.land = True
        self.id = id

    def __str__(self):
        return "Mountain, " + str(self.id)

    def canplay(self, boardstate):
        pass

    def shouldplay(self, boardstate):
        pass
