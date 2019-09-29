#! /usr/bin/python3
import argparse
import progressbar
import statistics
import itertools
from numpy import prod

from magic.card import Card
from magic.boardstate import Boardstate
from magic.decklist import Decklist
import rollout

parser = argparse.ArgumentParser(description='Automating MtG goldfishing')
parser.add_argument('--turns', '-t', type=int, default=20, help='Maximum number of turns per game')
parser.add_argument('--matches', '-m', type=int, default=50, help='Number of matches to simulate')
parser.add_argument('--iterations', '-i', type=int, default=25, help='When evaluating a hand, how many rollouts to try')
parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
parser.add_argument('--draw', '-d', action='store_true', help='Assume we\'re on the draw')
parser.add_argument('--life', '-l', type=int, default=20, help='Start opponent\'s life total at value')
args = parser.parse_args()

# Make our decklist
decklist = Decklist()

if args.verbose:
    print("=== Cards in deck:", len(decklist), "===")

# dict of scores by turn, including cascading mulls downward
final_turn_scores = {}
mulligan_stats = []

for mull_to in range(1, 8):
    turn_scores = []

    mull_count = 0
    for i in progressbar.progressbar(range(args.matches)):
        starting_hand = decklist.sample_hand(7)

        # For each card, calculate the average kill of mulling that card
        performance = 100
        for hand in itertools.combinations(starting_hand, mull_to):
            # Itertools gives us the hand we keep. Take the diff to get the cards we mulled
            cards_put_back = list(set(starting_hand) - set(hand))
            kill_turn = rollout.rollout_hand(decklist,
                                             hand,
                                             cards_put_back,
                                             iterations=args.iterations,
                                             verbose=args.verbose)
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
                mull_count += 1
        turn_scores.append(performance)

    turn_score_mean = statistics.mean(turn_scores)
    final_turn_scores[mull_to] = turn_score_mean
    mulligan_stats.append(mull_count / args.matches)
    print("Mulling to ", mull_to, " kills on turn:", round(turn_score_mean, 6))

print("\n============================")
print("Results!")
print("Mull stats:")
for i in range(len(mulligan_stats)):
    flip_one = list(mulligan_stats)
    flip_one[0] = 1 - flip_one[0]
    print("\tKept on", i+1, ": ", round(prod(flip_one) * 100, 6), "%")
    mulligan_stats.pop(0)

print("This list kills on average on turn: ", round(final_turn_scores[7], 6))
