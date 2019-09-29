# montecarlomagic
Automating goldfish games of Magic: The Gathering

By automating thousands of goldfished games of decks, we can find empirically correct deckbuilding answers!

## Caveats
This method has no opponent sitting across from you! Games of Magic: the Gathering are rarely won or lost in a vacuum. But for certain linear strategies, it's useful to see how your deck performs linearly, and then make sacrifices for interaction.

That said, we can stochastically simulate opponents. (Random turn 1 Thoughtseizes, spells being countered with some percent chance, etc...) [Not implemented yet]

## Usage

```
usage: montecarlomagic.py [-h] [--turns TURNS] [--matches MATCHES] [--verbose]
                          [--draw] [--life LIFE]

Automating MtG goldfishing

optional arguments:
  -h, --help            show this help message and exit
  --turns TURNS, -t TURNS
                        Maximum number of turns per game
  --matches MATCHES, -m MATCHES
                        Number of matches to simulate
  --iterations ITERATIONS, -i ITERATIONS
                        When evaluating a hand, how many rollouts to try
  --verbose, -v         Verbose output
  --draw, -d            Assume we're on the draw
  --life LIFE, -l LIFE  Start opponent's life total at value
```

## Sample Results for Modern Burn

### 20 Lands, standard burn list
```
./montecarlomagic.py -m 1000
Mull stats:
	Kept on 1 :  0.002188 %
	Kept on 2 :  0.544744 %
	Kept on 3 :  1.760797 %
	Kept on 4 :  6.114637 %
	Kept on 5 :  15.779834 %
	Kept on 6 :  33.6978 %
	Kept on 7 :  42.1 %
This list kills on average on turn:  4.365609
```

### What if we replaced Goblin Guide with lands?
```
Mull stats:
	Kept on 1 :  0.0 %
	Kept on 2 :  0.746123 %
	Kept on 3 :  2.311757 %
	Kept on 4 :  7.272795 %
	Kept on 5 :  17.144525 %
	Kept on 6 :  37.3248 %
	Kept on 7 :  35.2 %
This list kills on average on turn:  4.914534
```

Predictably, Burn performs better with the Goblin Guides in the deck!
