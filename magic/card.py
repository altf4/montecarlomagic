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
        self.name = ""
        self.priority = 0
        self.fetchable = False
        self.power = 0
        self.bonuspower = 0 # Temporary until end-of-turn bonus power
        self.summoning_sick = True
        self.tapsfor = defaultdict(lambda: False)
        self.cardtypes = defaultdict(lambda: False)
        self.keywords = defaultdict(lambda: False)

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

    def scoop(self, boardstate):
        """Reset this card back to it's original state. Undo any internal state changes
        """
        self.summoning_sick = True
        self.istapped = False

    @abstractmethod
    def canplay(self, boardstate):
        """Is this a legal play right now?
        """
        # If it's a land and we haven't played one yet
        if self.cardtypes["land"]:
            if boardstate.thisturn["playedland"] == False:
                return True
            else:
                return False
        return True

    @abstractmethod
    def play(self, boardstate):
        # Prowess triggers
        if self.cardtypes["instant"] or self.cardtypes["sorcery"]:
            for card in boardstate.battlefield:
                if card.keywords["prowess"]:
                    card.bonuspower += 1

        if self.cardtypes["land"]:
            boardstate.thisturn["playedland"] = True
            boardstate.hand.remove(self)
            boardstate.lands.append(self)
        elif self.cardtypes["creature"]:
            boardstate.hand.remove(self)
            boardstate.battlefield.append(self)
        else:
            boardstate.hand.remove(self)
            boardstate.graveyard.append(self)
