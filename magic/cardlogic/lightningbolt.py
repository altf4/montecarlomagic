from magic.card import Card

class LightningBolt(Card):
    def __init__(self, id):
        super().__init__(id)

    def __str__(self):
        return "Lightning Bolt, " + str(self.id)

    def canplay(self, boardstate):
        pass

    def shouldplay(self, boardstate):
        pass
