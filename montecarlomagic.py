#! /usr/bin/python3
import argparse
import progressbar
import statistics
import itertools

from magic.card import Card
from magic.boardstate import Boardstate
from magic.decklist import Decklist


parser = argparse.ArgumentParser(description='Automating MtG goldfishing')
parser.add_argument('--turns', '-t', type=int, default=20, help='Maximum number of turns per game')
parser.add_argument('--matches', '-m', type=int, default=100000, help='Matches to simulate')
parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
parser.add_argument('--draw', '-d', action='store_true', help='Assume we\'re on the draw')
parser.add_argument('--life', '-l', type=int, default=20, help='Start opponent\'s life total at value')
args = parser.parse_args()

def win_condition(boardstate):
    if boardstate.opponent_life <= 0:
        return True
    else:
        return False

def rollout_hand(decklist, hand_ids, cards_put_back, iterations=1000):
    """ Run iterations of the given hand
        Returns the average turn we kill on for this hand

        decklist: Decklist object to play
        hand_ids: A list of card IDs (not card objects)
        cards_put_back: List of card IDs to mull to bottom
        iterations: Number of times to play this hand
    """
    win_stats = []

    for i in range(iterations):
        # Create the boardstate
        boardstate = Boardstate(decklist,
                                opening_hand=hand_ids,
                                cards_put_back=cards_put_back,
                                starting_life=args.life)

        # Run the game
        for turn in range(1, args.turns+1):
            # Untap
            boardstate.untap()

            # Upkeep
            # Cast any cards on suspend:
            for card in boardstate.exile:
                if boardstate.autotapper(card.manacost(boardstate)):
                    card.play(boardstate)

            # Draw
            # Are we on the play or on the draw?
            if args.draw:
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
                if card.iscreature and not card.istapped and not card.summoning_sick:
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

            if args.verbose:
                print("=== Turn", turn, "===")
                print("Opponent's Life: ", boardstate.opponent_life)
                print("Battlefield:")
                for card in boardstate.battlefield:
                    print("\t", card)
                print("Lands:")
                for card in boardstate.lands:
                    print("\t", card)
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
            if win_condition(boardstate):
                win_stats.append(turn)
                boardstate.scoop()
                break

        # When we're at the end of the game, scoop
        win_stats.append(turn)
        boardstate.scoop()

    # Calculate stats
    return statistics.mean(win_stats)

# Make our decklist
decklist = Decklist()

if args.verbose:
    print("=== Cards in deck:", len(decklist), "===")

# dict of scores by turn, including cascading mulls downward
final_turn_scores = {}

for mull_to in range(1, 8):
    turn_scores = []

    for i in progressbar.progressbar(range(args.matches)):
        starting_hand = decklist.sample_hand(7)

        # For each card, calculate the average kill of mulling that card
        performance = 100
        for hand in itertools.combinations(starting_hand, mull_to):
            # Itertools gives us the hand we keep. Take the diff to get the cards we mulled
            cards_put_back = list(set(starting_hand) - set(hand))
            kill_turn = rollout_hand(decklist, hand, cards_put_back, iterations=args.matches)
            if kill_turn < performance:
                performance = kill_turn

        assert(performance < 100)
        # If this hand is worse than the average performance of mulling down
        #   Then assume we mull and get an average performance
        #   Except on one, always keep on one
        if mull_to > 1:
            # lower is better here, remember
            if performance > final_turn_scores[mull_to - 1]:
                performance = final_turn_scores[mull_to - 1]
        turn_scores.append(performance)

    turn_score_mean = statistics.mean(turn_scores)
    final_turn_scores[mull_to] = turn_score_mean
    print("Mulling to ", mull_to, " kills on turn:", round(turn_score_mean, 6))
