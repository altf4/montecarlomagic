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
Average Win on Turn:  5.51162
Mull stats:
	Kept on 7 81.75%
	Kept on 6 15.256%
	Kept on 5 2.455%
	Kept on 4 0.539%
	Scried top: 55.51%
```

### 22 Lands
```
./montecarlomagic.py -t 15 -m 100000
Average Win on Turn:  5.69706
Mull stats:
	Kept on 7 75.271%
	Kept on 6 20.225%
	Kept on 5 3.83%
	Kept on 4 0.674%
	Scried top: 56.93%
```

Predictably, Burn performs better with 18 lands than 22!

## Mulligan Decisions

### Always Mull 3+ Land Hands (But keep on 4)

```
./montecarlomagic.py -t 15 -m 100000
Average Win on Turn:  5.68888
Mull stats:
	Kept on 7 58.017%
	Kept on 6 27.2%
	Kept on 5 10.268%
	Kept on 4 4.515%
	Scried top: 51.06%
```

### Always Mull 4+ Land Hands (But keep on 4)

```
./montecarlomagic.py -t 15 -m 100000
Average Win on Turn:  5.51162
Mull stats:
	Kept on 7 81.75%
	Kept on 6 15.256%
	Kept on 5 2.455%
	Kept on 4 0.539%
	Scried top: 55.51%
```

### Mull 4+ Land Hands, but Keep No-Land'ers
```
./montecarlomagic.py -t 15 -m 100000
Average Win on Turn:  5.73129
Mull stats:
	Kept on 7 88.722%
	Kept on 6 10.584%
	Kept on 5 0.682%
	Kept on 4 0.012%
	Scried top: 54.8%
```
