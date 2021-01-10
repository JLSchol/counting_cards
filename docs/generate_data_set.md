# how to generate the data set
Keep it simple
Train specific on Unibet blackjack table
just train on 

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


### option 1
- 