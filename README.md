# montecarlomagic
Automating goldfish games of Magic: The Gathering

By automating thousands of goldfished games of decks, we can find empirically correct deckbuilding answers!

## Caveats
This method has no opponent sitting across from you! Games of Magic: the Gathering are rarely won or lost in a vacuum. But for certain linear strategies, it's useful to see how your deck performs linearly, and then make sacrifices for interaction.

That said, we can stochastically simulate opponents. (Random turn 1 Thoughtseizes, spells being countered with some percent chance, etc...) [Not implemented yet]

## Usage

```
montecarlomagic.py [-h] [--turns TURNS] [--matches MATCHES] [--verbose] [--draw]

optional arguments:
  -h, --help            show this help message and exit
  --turns TURNS, -t TURNS
                        Maximum number of turns per game
  --matches MATCHES, -m MATCHES
                        Matches to simulate
  --verbose, -v         Verbose output
  --draw, -d            Assume we're on the draw
```

## Sample Results for Modern Burn
(Just Mountains and Bolts. Not a fully legal decklist yet)

### 18 Lands
```
./montecarlomagic.py -t 15 -m 100000
Average Win on Turn:  5.55662
Mull stats:
	Kept on 7 81.964%
	Kept on 6 15.051%
	Kept on 5 2.447%
	Kept on 4 0.538%
```

### 22 Lands
```
./montecarlomagic.py -t 15 -m 100000
Average Win on Turn:  5.76035
Mull stats:
	Kept on 7 74.908%
	Kept on 6 20.542%
	Kept on 5 3.852%
	Kept on 4 0.698%
```

Predictably, Burn performs better with 18 lands than 22!

## Mulligan Decisions

### Always Mull 3+ Land Hands (But keep on 4)

```
./montecarlomagic.py -t 15 -m 100000
Average Win on Turn:  5.77248
Mull stats:
	Kept on 7 58.335%
	Kept on 6 26.994%
	Kept on 5 10.093%
	Kept on 4 4.578%
```

### Always Mull 4+ Land Hands (But keep on 4)

```
./montecarlomagic.py -t 15 -m 100000
Average Win on Turn:  5.55661
Mull stats:
	Kept on 7 81.722%
	Kept on 6 15.257%
	Kept on 5 2.483%
	Kept on 4 0.538%
```

### Mull 4+ Land Hands, but Keep No-Land'ers
(Vancouver-scry not yet implemented, so maybe this performs better actually)

```
Average Win on Turn:  5.76094
Mull stats:
	Kept on 7 88.817%
	Kept on 6 10.515%
	Kept on 5 0.649%
	Kept on 4 0.019%
```
