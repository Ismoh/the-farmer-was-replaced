# The Farmer Was Replaced 1.0

My 2 cents to TFWR coding challenges.

I realised after 24,2h.. classes won't be available.

I am not into python or modular coding, that's why the code might be a bit weird to read, but works like a charm. You can see OOP and inheritance patterns, but nevermind.

Full automation has higher prio then code challenge snippets, that's why you aren't able to run specific challenges in scripts. I'll change that in future.

## Challenges

### `main.py`

Fully automated to unlock Unlocks. If `Auto Unlocks` isn't unlocked yet, you can simply set a goal manually:
https://github.com/Ismoh/the-farmer-was-replaced/blob/e8f03c84bba5b6b49b5a78ec78e1312d1dc46836/main.py#L50-L52

### `bones.py`

TBC

### `cacti.py`

TBC

### `carrots.py`

As well fully automated.\
KISS: Check costs, harvest costs beforehand if needed, plant and harvest.\
It unlocks any Carrot Unlock by itself.

### `hay.py`

As well fully automated.\
KISS: Check costs, harvest costs beforehand if needed, plant and harvest.\
It unlocks any Hay Unlock by itself.
> there's no plural of hay - (╯°□°)╯︵ ┻━┻

### `mazes.py`

I used DFS algorithm with cache to max out gold crop by 300 maze runs in a row.\
Maximum of get_world_size() is split into smaller squares based on amout of drones.\
As well fully automated.\
KISS: Check costs, harvest costs beforehand if needed, plant and harvest.\
It unlocks any Gold Unlock by itself.

### `movement.py`

KISS principle: move to x, y

### `pumpkins.py`

KISS principle: Check costs, harvest costs beforehand if needed, plant (the whole farm), wait if dead pumpkin, fix, repeat.\
I did some rough time measurements and came to the conclusion that waiting is the best solution to get rid of Dead_Pumpkins.\
Maximum crop per run.

### `unlocks.py`

Fetch all Unlocks and filter by costs and item weight. Take a look on the example on the bottom: [Usage](#usage).

### `weird_substances.py`

As well fully automated.\
KISS: Check costs, harvest costs beforehand if needed, plant and harvest.\
It would also unlock any possible Weird_Substance Unlock by itself, if there would be any.

### `woods.py`

As well fully automated.\
KISS: Check costs, harvest costs beforehand if needed, plant and harvest.\
It unlocks any Wood Unlock by itself.\
`TODO: Need to add trees.`

## Usage

Run main.py and that's it - unless the needed Unlocks were unlocked manually.\
It's fully automated to unlock all Unlocks sorted by lowest costs prioritisation of entity weight considered.\
Entity weight (or costs order) is how easy it is to get the associated item.\
Weight is currently define by best guess.

| Unlock           | Level | Costs | Item   | Weight |
| ---------------- | ----- | ----- | ------ | ------ |
| Unlocks.Watering | 6     | 51200 | Wood   | 1      |
| Unlocks.Pumpkins | 4     | 16000 | Carrot | 2      |

Wood is easier to farm instead of Carrot and so on.

## Improvements

- unlock all Unlocks
- HayLeaderbords TBC
- Bones TBC
- Optimization: Performance testing and algorithm comparison - TBC
