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
  --verbose, -v         Verbose output
  --draw, -d            Assume we're on the draw
  --life LIFE, -l LIFE  Start opponent's life total at value
```

## Sample Results for Modern Burn
(Almost all the cards implemented. Just missing a couple)

### 18 Lands
```
./montecarlomagic.py -m 160
Mull stats:
	Kept on 1 :  0.108668 %
	Kept on 2 :  2.375173 %
	Kept on 3 :  3.926071 %
	Kept on 4 :  10.9729 %
	Kept on 5 :  17.382812 %
	Kept on 6 :  27.734375 %
	Kept on 7 :  37.5 %
This list kills on average on turn:  4.653703
```

### 22 Lands
```
./montecarlomagic.py -m 160
Mull stats:
	Kept on 1 :  0.041891 %
	Kept on 2 :  1.633764 %
	Kept on 3 :  3.581303 %
	Kept on 4 :  8.761597 %
	Kept on 5 :  24.65332 %
	Kept on 6 :  30.078125 %
	Kept on 7 :  31.25 %
This list kills on average on turn:  4.728068
```

Predictably, Burn performs better with 18 lands than 22!
