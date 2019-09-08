import csv
from collections import defaultdict
from abc import ABC, abstractmethod
from magic.manacost import ManaCost


class Card(ABC):
    """ Abstract class for a card. All cards inherit from this
    """
    def __init__(self, id):
        self.id = id
        self.istapped = False
        self.ishistoric = False
        self.name = ""
        self.priority = 0
        self.legendary = 0
        self.land = False
        self.fetchable = False
        self.power = 0
        self.summoning_sick = True
        self.iscreature = False
        self.tapsfor = defaultdict(lambda: False)

    def __str__(self):
        return self.name

    @abstractmethod
    def manacost(self, boardstate):
        """What's the mana cost of the spell right now?
        """
        pass

    @abstractmethod
    def shouldplay(self, boardstate):
        """Is this a card we should play right now?
        """
        pass

    @abstractmethod
    def canplay(self, boardstate):
        """Is this a legal play right now?
        """
        # If it's a land and we haven't played one yet
        if self.land:
            if boardstate.thisturn["playedland"] == False:
                return True
            else:
                return False
        return True

    @abstractmethod
    def play(self, boardstate):
        if self.land:
            boardstate.thisturn["playedland"] = True
            boardstate.hand.remove(self)
            boardstate.lands.append(self)
        elif self.iscreature:
            boardstate.hand.remove(self)
            boardstate.battlefield.append(self)
        else:
            boardstate.hand.remove(self)
            boardstate.graveyard.append(self)
