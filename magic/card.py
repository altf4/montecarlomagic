import csv
from abc import ABC, abstractmethod
from magic.manacost import ManaCost

class Card(ABC):
    istapped = False
    ishistoric = False
    name = ""
    priority = 0
    legendary = 0
    land = False
    id = -1
    tapsfor = {}

    def __init__(self, id):
        self.id = id
        self.tapsfor["white"] = True
        self.tapsfor["blue"] = True
        self.tapsfor["black"] = True
        self.tapsfor["red"] = True
        self.tapsfor["green"] = True
        self.tapsfor["colorless"] = True

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
        else:
            return True
        return True

    @abstractmethod
    def play(self, boardstate):
        if self.land:
            boardstate.thisturn["playedland"] = True
            # Remove the card from hand
            boardstate.hand.remove(self)
            boardstate.lands.append(self)
        else:
            # Remove the card from hand
            boardstate.hand.remove(self)
            boardstate.graveyard.append(self)
