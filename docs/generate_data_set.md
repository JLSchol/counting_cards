# how to generate the data set
Keep it simple
Train specific on Unibet blackjack table
just train on 

Explanation convolutional neural networks:
- what is a neural network
- (input,convolutional, pooling, flatting) layers
- hyper parameters
- Activation functions
https://poloclub.github.io/cnn-explainer/

## Considerations
- detect whole card vs corners/sides
- detect only value vs type and value
- generate data set and label automatically vs
- Which labels do we use, only cards facing up?, also table, dealer, player positions?


### decisions
- only label value and closed card
- generate data set

## Creating data set
1. Acquire template data
2. Generate data set

### Acquire raw data
- crop every card (type+value, back of card)
- get different empy backgrounds
- create different overlapping card situations

### generating data set



for each card randomize:
- shape
- side of object 
- relative size
- angle of rotation
- tilt 
- illumination


### How to represent cards
- single cards 53 (for x card and 3 casino backgrounds?)
	- 8 table positions
	- 6 rotations (Somewhere on the table)
	- 4 blocked corners (random orientation, position, warped at the table)
	- 4 blocked sides (random orientation, position, warped at the table)

- corner overlap (4 cards)
- top overlap (4 cards)
- side overlap (4 cards)

