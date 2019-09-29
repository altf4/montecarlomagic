from magic.card import Card
from magic.manacost import ManaCost

class RiftBolt(Card):
    def __init__(self, id):
        super().__init__(id)
        # High priority. We want to get rid of these pretty quick
        self.priority = 80
        self._suspended = False
        self.name = "Rift Bolt"
        self.cardtypes["sorcery"] = True

    def __str__(self):
        suspended = ""
        if self._suspended:
            suspended = " [Suspended]"
        return "Rift Bolt, " + str(self.id) + suspended

    def scoop(self, boardstate):
        super().scoop(boardstate)
        self._suspended = False

    def canplay(self, boardstate):
        # Check for normal conditions
        return super().canplay(boardstate)

    def shouldplay(self, boardstate):
        # Always just play if we can
        return True

    def manacost(self, boardstate):
        # The spell casts for free from suspend
        if self._suspended:
            return ManaCost("0")
        # If we can pay full price, do it
        if boardstate.autotapper(ManaCost("2r"), True):
            return ManaCost("2r")
        return ManaCost("r")

    def play(self, boardstate):
        # Get the ManaCost of the spell. That determines how we play it
        cost = self.manacost(boardstate)

        # Suspend the card
        if str(cost) == "r":
            self._suspended = True
            # Put into exile
            boardstate.hand.remove(self)
            boardstate.exile.append(self)
            return

        if str(cost) == "0":
            boardstate.exile.remove(self)
            boardstate.graveyard.append(self)
            self._suspended = False
            boardstate.opponent_life -= 3
            return

        self._suspended = False
        boardstate.opponent_life -= 3
        super().play(boardstate)
