#! /usr/bin/python3
import argparse
import mulligan

from magic.card import Card
from magic.boardstate import Boardstate
from magic.decklist import Decklist


parser = argparse.ArgumentParser(description='Automating MtG goldfishing')
parser.add_argument('--turns', '-t', type=int, default=10, help='Maximum number of turns per game')
parser.add_argument('--matches', '-m', type=int, default=100000, help='Matches to simulate')
parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
parser.add_argument('--draw', '-d', action='store_true', help='Assume we\'re on the draw')
args = parser.parse_args()

decklist = Decklist()
boardstate = Boardstate(decklist)

if args.verbose:
    print("=== Cards in deck:", len(decklist), "===")

def win_condition(boardstate):
    if boardstate.opponent_life <= 0:
        return True
    else:
        return False

mull_stats = {}
for i in range(8):
    mull_stats[i] = 0
scry_top_count = 0

win_stats = {}
for i in range(args.turns+1):
    win_stats[i] = 0

for match in range(args.matches):
    handsize = 7

    # Draw starting hand
    boardstate.draw(handsize)

    while handsize > 0 and mulligan.mulligan_burn(boardstate.hand):
        handsize -= 1
        boardstate.scoop()
        boardstate.draw(handsize)

    if handsize < 7:
        scry_top = mulligan.scry_burn(boardstate.hand, boardstate.library[0])
        if not scry_top:
            card = boardstate.library.pop(0)
            boardstate.library.append(card)
        else:
            scry_top_count += 1

    # Gather some stats on mulligans
    mull_stats[handsize] += 1

    # Max of args.turns turns per game
    for turn in range(args.turns):
        # Untap
        boardstate.untap()

        # Upkeep
        # Cast any cards on suspend:
        for card in boardstate.exile:
            if boardstate.autotapper(card.manacost(boardstate)):
                card.play(boardstate)

        # Are we on the play or on the draw?
        if args.draw:
            boardstate.draw(1)
        else:
            if turn > 0:
                boardstate.draw(1)

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

        if args.verbose:
            print("=== Turn", turn+1, "===")
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
            win_stats[turn+1] += 1
            boardstate.scoop()
            break

    # When we're at the end of the game, scoop
    boardstate.scoop()

# Print stats
total_count, total = 0, 0
for turn, count in win_stats.items():
    total += turn * count
    total_count += count

print("Average Win on Turn: ", round(total / total_count, 5))

print("Mull stats:")
for handsize, count in mull_stats.items():
    if mull_stats[7-handsize] > 0:
        print("\tKept on", 7-handsize, str(round((mull_stats[7-handsize] / args.matches)*100, 6)) + "%")

mull_total = args.matches - mull_stats[7]
print("\tScried top:", str(round((scry_top_count / mull_total)*100, 2)) + "%")
