from magic.card import Card
from magic.manacost import ManaCost

from random import shuffle

class AridMesa(Card):
    def __init__(self, id):
        super().__init__(id)
        self.land = True
        self.id = id
        self.priority = 100
        self.name = "Arid Mesa"

    def __str__(self):
        return "Arid Mesa, " + str(self.id)

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
            tapsforcount = sum(card.tapsfor.values())
            if card.land and card.fetchable and (tapsforcount > 1):
                boardstate.library.remove(card)
                boardstate.lands.append(card)
                shuffle(boardstate.library)
                return
        # If not, get a basic
        for card in boardstate.library:
            if card.land and card.fetchable and (card.tapsfor["red"] or card.tapsfor["white"]):
                boardstate.library.remove(card)
                boardstate.lands.append(card)
                shuffle(boardstate.library)
                return
