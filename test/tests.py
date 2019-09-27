#! /usr/bin/python3

import unittest
import random
from collections import Counter

from magic.card import Card
from magic.boardstate import Boardstate
from magic.decklist import Decklist
import rollout

class ImportTest(unittest.TestCase):
    def setUp(self):
        # Make our decklist
        self.decklist = Decklist("test/burn_decklist.txt")

    def test_burn_decklist_correct(self):
        """Test that the decklist was imported correctly
        """
        # Get a sample library
        library = self.decklist.get_library()
        self.assertEqual(len(library), 60)
        # Check indices
        index = 1
        for card in library:
            self.assertEqual(card.id, index)
            index += 1

        # Check names
        cardcounts = Counter(card.name for card in library)
        self.assertEqual(cardcounts["Mountain"], 2)
        self.assertEqual(cardcounts["Sunbaked Canyon"], 4)
        self.assertEqual(cardcounts["Inspiring Vantage"], 4)
        self.assertEqual(cardcounts["Wooded Foothills"], 2)
        self.assertEqual(cardcounts["Arid Mesa"], 4)
        self.assertEqual(cardcounts["Sacred Foundry"], 2)
        self.assertEqual(cardcounts["Lightning Bolt"], 10)
        self.assertEqual(cardcounts["Skullcrack"], 4)
        self.assertEqual(cardcounts["Boros Charm"], 4)
        self.assertEqual(cardcounts["Lava Spike"], 4)
        self.assertEqual(cardcounts["Rift Bolt"], 4)
        self.assertEqual(cardcounts["Goblin Guide"], 4)
        self.assertEqual(cardcounts["Eidolon Of The Great Revel"], 4)
        self.assertEqual(cardcounts["Lightning Helix"], 4)
        self.assertEqual(cardcounts["Skewer The Critics"], 4)


class RolloutTest(unittest.TestCase):
    def setUp(self):
        # Make our decklist
        self.decklist = Decklist("test/burn_decklist.txt")

    def test_burn_sample_hands_performance(self):
        random.seed(12345)
        performance = rollout.rollout_hand(self.decklist,
                                           [1, 2, 3, 4, 5, 6, 7],
                                           [],
                                           iterations=10)
        self.assertEqual(performance, 9.4)
        performance = rollout.rollout_hand(self.decklist,
                                           [34, 21, 1, 5, 7],
                                           [32, 59],
                                           iterations=10)
        self.assertEqual(performance, 7.8)

if __name__ == '__main__':
    unittest.main()
