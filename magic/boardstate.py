from random import shuffle
from magic.manacost import ManaCost


class Boardstate():
    def __init__(self, decklist, opening_hand=None, cards_put_back=None, starting_life=20):
        self.graveyard = []
        self.battlefield = []
        self.hand = []
        self.lands = []
        self.exile = []
        self.opponent_life = 20
        self.life = 20
        # Dict of flags (default false) affecting the gamestate this turn
        self.thisturn = {}
        self.thisturn["playedland"] = False
        self.decklist = decklist
        self.library = self.decklist.get_library()
        # Make a copy of the list of cards. We'll use it later to reset the boardstate
        self._allcards = list(self.library)
        self.starting_life = starting_life
        for card_id in opening_hand:
            # Search library for that ID
            for library_card in self.library:
                if library_card.id == card_id:
                    # Move to hand
                    self.hand.append(library_card)
                    self.library.remove(library_card)
                    break
        shuffle(self.library)
        for card in cards_put_back:
            # Search library for that ID
            for library_card in self.library:
                if library_card.id == card_id:
                    # Move to bottom of library
                    self.library.remove(library_card)
                    self.library.append(library_card)
                    break

    def scoop(self):
        """Reset the gamestate to all cards in library
        """
        self.library = list(self._allcards)
        shuffle(self.library)
        for card in self.library:
            card.scoop(self)
        self.graveyard = []
        self.battlefield = []
        self.hand = []
        self.lands = []
        self.exile = []
        self.untap()
        self.opponent_life = self.starting_life
        self.life = self.starting_life

    def draw(self, amount=1):
        if amount > len(self.library):
            return False
        for i in range(amount):
            self.hand.append(self.library[0])
            del [self.library[0]]
        return True

    def untap(self):
        # Reset "end of turn" flags
        self.thisturn = dict.fromkeys(self.thisturn, False)
        self.opponent_life_start_turn = self.opponent_life

        for card in self.lands:
            card.istapped = False
        for card in self.battlefield:
            card.istapped = False
            card.summoning_sick = False

    def cleanup(self):
        # TODO: Discard to hand size
        pass

    def autotapper(self, cost, test=False):
        """Tap lands to pay for spells
        Returns whether this succeeded or not. False means the spell didn't cast
        """
        # For spells, check if we have the right mana
        tap_queue = []

        # Get a list of all the available mana producers out right now
        mana_producers = []
        for card in self.lands:
            if not card.istapped:
                mana_producers.append(card)

        # Do we have enough raw mana?
        if cost.cmc > len(mana_producers):
            return False

        # Try to spend low priority lands first
        mana_producers.sort(key=lambda x: x.priority, reverse=True)

        # Do we have the colors?
        for color in cost.colors:
            while cost.colors[color] > 0:
                keepgoing = False
                # Remove a source from the list of producers
                for card in mana_producers:
                    if card.tapsfor[color]:
                        mana_producers.remove(card)
                        tap_queue.append(card)
                        cost.colors[color] -= 1
                        keepgoing = True
                # if we didn't find a land, we don't have the color
                if keepgoing == False:
                    return False
        # Pay for the remaining colorless
        while cost.colorless > 0:
            keepgoing = False
            # Remove a source from the list of producers
            for card in mana_producers:
                mana_producers.remove(card)
                tap_queue.append(card)
                cost.colorless -= 1
                keepgoing = True
            # if we didn't find a land, we don't have the mana
            if keepgoing == False:
                return False

        if cost.colors["red"] + cost.colors["blue"] + \
            cost.colors["white"] + cost.colors["black"] + \
            cost.colors["green"] + cost.colorless > 0:
            return False

        # Okay, now actually tap the Lands
        if not test:
            for land in tap_queue:
                land.istapped = True
        return True

    def destroy(self, card):
        """ Destroy (or sacrifice) given permanent on the battlefield
        """
        if card.land:
            self.lands.remove(card)
        else:
            self.battlefield.remove(card)
        self.graveyard.append(card)

    def attackwith(self, card):
        """ Attack opponent with the given card
        """
        assert(card.iscreature)
        card.istapped = True
        self.opponent_life -= card.power
