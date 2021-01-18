import random

class Card():
	def __init__(self, rank, suit, value=None):
		self.rank = str(rank)
		self.suit = str(suit)
		self.id = rank+suit
		self.value = value

	def show(self):
		print("{} of value: {}\n".format(self.id, self.value))


class Deck():
	def __init__(self, nr_decks=1):
		self.nr_decks = nr_decks
		self.suits = ['h', 'd', 's', 'c']
		self.ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
		self.values = list(range(2,11)) + 3*[10] + [(1,11)]
		self.cards = []
		self.discards = []
		self._build()

	def _build(self):
		for deck in range(self.nr_decks):
			for suit in self.suits:
				for rank, value in zip(self.ranks,self.values):
						self.cards.append(Card(rank,suit,value))

	def shuffle(self):
		random.shuffle(self.cards)
		self.discards = []
		return self
	
	def show(self, what='cards'):
		cards = []
		if what == 'cards':
			cards = self.cards
		elif what == 'discards':
			cards = self.discards
		for card in cards:
			card.show()

	def drawCard(self):
		return self.cards.pop()

	def discardCard(self, card):
		self.discards.append(card)

	def reset(self, nr_decks=1):
		self.__init__(nr_decks)
		return self



def main():
	print("Show initialized deck:")
	deck = Deck(1)
	deck.show()

	print("\nshuffle and show deck:")
	deck.shuffle()
	deck.show()

	print('\nDraw 2 cards show:')
	card1 = deck.drawCard()
	card2 = deck.drawCard()
	card1.show()
	card2.show()

	print('\nDiscard card and show discarded cards')
	deck.discardCard(card1)
	deck.show('discards')

	print("\nReset deck, shuffle and show deck + discards")
	deck.reset(1).shuffle()
	print('deck:')
	deck.show()
	print('discards:')
	deck.show('discards')



	
if __name__ == '__main__':
	main()
