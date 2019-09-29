from magic.card import Card
from magic.boardstate import Boardstate
from magic.decklist import Decklist

import statistics


def _win_condition(boardstate):
    if boardstate.opponent_life <= 0:
        return True
    else:
        return False

def rollout_hand(decklist,
                 hand_ids,
                 cards_put_back,
                 iterations=100,
                 max_turns=15,
                 starting_life=20,
                 on_the_draw=False,
                 verbose=False):
    """ Run iterations of the given hand
        Returns the average turn we kill on for this hand

        decklist: Decklist object to play
        hand_ids: A list of card IDs (not card objects)
        cards_put_back: List of card IDs to mull to bottom
        iterations: Number of times to play this hand
        max_turns: The maximum number of turns before giving up
        starting_life: Opponent's starting life
        on_the_draw: Are we on the draw?
        verbose: Verbose debug printing. Very verbose
    """
    win_stats = []

    for i in range(iterations):
        # Create the boardstate
        boardstate = Boardstate(decklist,
                                opening_hand=hand_ids,
                                cards_put_back=cards_put_back,
                                starting_life=starting_life)

        # Run the game
        for turn in range(1, max_turns+1):
            # Untap
            boardstate.untap()

            # Upkeep
            # Cast any cards on suspend:
            for card in boardstate.exile:
                if boardstate.autotapper(card.manacost(boardstate)):
                    card.play(boardstate)

            # Draw
            # Are we on the play or on the draw?
            if on_the_draw:
                boardstate.draw(1)
            else:
                if turn > 1:
                    boardstate.draw(1)

            # Main Phase 1
            # Play the highest priority thing in our hand
            # Sort hand by priority
            keepgoing = True
            while keepgoing:
                boardstate.hand.sort(key=lambda x: x.priority, reverse=True)
                keepgoing = False
                for card in boardstate.hand:
                    # What is our highest priority card to play?
                    if card.canplay(boardstate):
                        if boardstate.autotapper(card.manacost(boardstate)):
                            card.play(boardstate)
                            keepgoing = True
                            break

            # Activate any abilities second

            # Attack
            for card in boardstate.battlefield:
                not_summoning_sick = (not card.summoning_sick) or (card.keywords["haste"])
                if card.cardtypes["creature"] and not card.istapped and not_summoning_sick:
                    boardstate.attackwith(card)

            # Main Phase 2
            # Play the highest priority thing in our hand
            # Sort hand by priority
            keepgoing = True
            while keepgoing:
                boardstate.hand.sort(key=lambda x: x.priority, reverse=True)
                keepgoing = False
                for card in boardstate.hand:
                    # What is our highest priority card to play?
                    if card.canplay(boardstate):
                        if boardstate.autotapper(card.manacost(boardstate)):
                            card.play(boardstate)
                            keepgoing = True
                            break

            if verbose:
                print("=== Turn", turn, "===")
                print("Opponent's Life: ", boardstate.opponent_life)
                print("Battlefield:")
                for card in boardstate.battlefield:
                    print("\t", card)
                print("Lands:")
                for card in boardstate.lands:
                    print("\t", card, "tapped:", card.istapped)
                print("Hand:")
                for card in boardstate.hand:
                    print("\t", card)
                print("Graveyard:")
                for card in boardstate.graveyard:
                    print("\t", card)
                print("Exile:")
                for card in boardstate.exile:
                    print("\t", card)
                print("\n")

            # Have we won?
            if _win_condition(boardstate):
                win_stats.append(turn)
                boardstate.scoop()
                break

        # When we're at the end of the game, scoop
        win_stats.append(turn)
        boardstate.scoop()

    # Calculate stats
    return statistics.mean(win_stats)
