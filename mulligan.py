
def mulligan_burn(hand):
    """ Should we mulligan this hand?
            Playing as burn
    """
    landcount = 0
    for card in hand:
        if card.land:
            landcount += 1

    # Keep any 4
    if len(hand) <= 4:
        return False

    # Mull the no-lander and all-land
    if landcount == 0 or (landcount == len(hand)):
        return True

    # If we just have too many lands, mull
    if landcount >= 4:
        return True

    if len(hand) == 5:
        pass
    if len(hand) == 6:
        pass
    if len(hand) == 7:
        pass

    # Otherwise, keep
    return False
