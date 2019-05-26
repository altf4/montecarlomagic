import csv
from abc import ABC, abstractmethod


class ManaCost():
    cmc = 0
    red = 0
    blue = 0
    white = 0
    green = 0
    black = 0
    colorless = 0
    devoid = False

    def __init__(self, cost_string):
        if cost_string[0].isdigit():
            self.colorless = int(cost_string[0])
        self.red = cost_string.count("r")
        self.blue = cost_string.count("u")
        self.white = cost_string.count("w")
        self.black = cost_string.count("b")
        self.green = cost_string.count("g")

        self.cmc = self.red + self.blue + self.white + self.black + self.green + self.colorless
        if self.red + self.blue + self.white + self.black + self.green == 0:
            self.devoid = True

class Card(ABC):
    istapped = False
    ishistoric = False
    name = ""
    priority = 0
    legendary = 0
    land = False
    id = -1

    def __init__(self, id):
        self.id = id
        # Look up the card name in the db
        #self.attrs = carddb[self.name]
        #self.priority = int(self.attrs["cast_priority"])

    def __str__(self):
        return self.name

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
        if self.attrs["type"] == "land" and not boardstate.playedland:
            print("trying to play land:", self, boardstate.playedland)
            return True
        else:
            # For spells, check if we have the right mana
            cost = ManaCost(self.attrs["mana_cost"])

            # Get a list of all the available mana producers out right now
            mana_producers = []
            for card in boardstate.lands:
                if not card.istapped:
                    mana_producers.append(Land(card.name))

            #   Do we have enough raw mana?
            if cost.cmc > len(mana_producers):
                return False
            #   Do we have the colors?
            while cost.blue > 0:
                keepgoing = False
                # Remove a blue source from the list of producers
                #   Try to spend low priority lands first
                mana_producers.sort(key=lambda x: x.priority, reverse=True)
                for card in mana_producers:
                    if card.blue:
                        mana_producers.remove(card)
                        cost.blue -= 1
                        keepgoing = True
                # if we didn't find a land, we don't have the color
                if keepgoing == False:
                    return False

            if cost.red + cost.blue + cost.white + cost.black + cost.green == 0:
                return True

        return False

    def play(self, boardstate):
        if self.attrs["type"] == "land":
            print("Plalying land: ", self, boardstate.playedland)
            boardstate.playedland = True
            # Remove the card from hand
            boardstate.hand.remove(self)
            boardstate.lands.append(self)
        else:
            print("casting spell", card)
