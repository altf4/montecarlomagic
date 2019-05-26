#! /usr/bin/python3
import argparse
import mulligan

from magic.card import Card
from magic.boardstate import Boardstate
from magic.decklist import Decklist


parser = argparse.ArgumentParser(description='Automating MtG goldfishing')
parser.add_argument('--turns', '-t', type=int, default=10, help='Maximum number of turns per game')
parser.add_argument('--matches', '-m', type=int, default=100000, help='Matches to simulate')
parser.add_argument('--verbose', '-v', type=bool, default=False, help='Verbose output')
args = parser.parse_args()

def printcardlist(cards):
    for card in cards:
        print(card)

decklist = Decklist()
boardstate = Boardstate(decklist)

if args.verbose:
    print("=== Cards in deck:", len(decklist), "===")

mull_stats = {}
mull_stats[7] = 0
mull_stats[6] = 0
mull_stats[5] = 0
mull_stats[4] = 0

for match in range(args.matches):
    handsize = 7

    # Draw starting hand
    boardstate.draw(handsize)

    while handsize > 0 and mulligan.mulligan_burn(boardstate.hand):
        handsize -= 1
        boardstate.scoop()
        boardstate.draw(handsize)

    # Gather some stats on mulligans
    mull_stats[handsize] += 1


    # Max of 10 turns per match
    for turn in range(args.turns):
        # Untap
        boardstate.untap()

        # Draw
        if turn > 0:
            boardstate.draw(1)

        # Play the highest priority thing in our hand
        # Sort hand by priority
        boardstate.hand.sort(key=lambda x: x.priority, reverse=True)
        for card in boardstate.hand:
            # What is our highest priority card to play?
            if card.canplay(boardstate):
                card.play(boardstate)

        if args.verbose:
            print("=== Turn", turn+1, "===")
            print("Battlefield:")
            for card in boardstate.battlefield:
                print("\t", card)
            print("Lands:")
            for card in boardstate.lands:
                print("\t", card)
            print("Hand:")
            for card in boardstate.hand:
                print("\t", card)
            print("\n")

    # When we're at the end of the game, scoop
    boardstate.scoop()

# Print stats
print(mull_stats)
print("Mull stats:")
print("Kept on 7: ", str(round((mull_stats[7] / args.matches)*100, 6)) + "%")
print("Kept on 6: ", str(round((mull_stats[6] / args.matches)*100, 6)) + "%")
print("Kept on 5: ", str(round((mull_stats[5] / args.matches)*100, 6)) + "%")
print("Kept on 4: ", str(round((mull_stats[4] / args.matches)*100, 6)) + "%")
