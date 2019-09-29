from magic.card import Card
from magic.manacost import ManaCost

from random import shuffle

class WoodedFoothills(Card):
    def __init__(self, id):
        super().__init__(id)
        self.cardtypes["land"] = True
        self.id = id
        self.priority = 100
        self.name = "Wooded Foothills"

    def __str__(self):
        return "Wooded Foothills, " + str(self.id)

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
        # fetch immediately
        boardstate.destroy(self)
        # Is there a dual land we can get first?
        for card in boardstate.library:
            # TODO ASSUME that all our fetchable duals can be fetched
            if card.cardtypes["land"] and card.fetchable and (len(card.tapsfor) > 1):
                boardstate.library.remove(card)
                boardstate.lands.append(card)
                shuffle(boardstate.library)
                return
        # If not, get a basic
        for card in boardstate.library:
            if card.cardtypes["land"] and card.fetchable and (card.tapsfor["red"] or card.tapsfor["green"]):
                boardstate.library.remove(card)
                boardstate.lands.append(card)
                shuffle(boardstate.library)
                return
