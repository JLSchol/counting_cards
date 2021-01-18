from deck_of_cards import Deck, Card

class Hand(object):
	''' Hand of cards in a black jack game, which keeps track of cards and their combined meaning in the context of BJ'''
	def __init__(self):
		self.cards = []			# list of Card objects
		self.ranks = []			# list of ranks ['Q','7',A,..]
		self.suits = []			# list of suits ['h','c',s,..] (h=hearts,d=dimons,c=cloves,s=spades)
		self.ids = []			# list of combined rank+suit  ['Qh','7c',As]
		self.values = []		# list of assigned values to card [10,7,(11/1),..]
		self.total = 0			# max score of <= 21 corrected for Ace1/11
		self.is_soft = False	# indicate that the max score is a soft hand or not (contains Ace of value 11)
		self.is_bj = False		# indicate that the hand is a black jack
		self.is_busted = False	# indicates that the player was busted (= selft.total>21)
		self.is_standed = False # indicates that the player standed on this hand
		self.is_closed = False	# if closed True, hand can not accept any more cards an hand is 'full/closed'

	def addCard(self, card):
		# check if we can draw cards
		if self.is_closed == True: # or self.__isTwentyOne() == True:
			print("Hand is closed, can not draw any more cards")
			return
		# update the hand with a single cards
		self.__updateHand(card)
		# update the total count from a single card
		self.__updateTotal(card)
		# check for blackjack
		if self.__isBlackJack():
			self.is_bj = True
			self.is_closed = True
			return
		# check for 21
		if self.__isTwentyOne():
			self.is_closed = True
			return
		# If total is over 21, it might contains aces. Find max value below 21
		self.__correctForSoftAce()
		# If after correction total is still over 21, set hand to busted
		if self.__isBusted():
			self.is_busted = True
			self.is_closed = True
			return

	def splitCard(self, card_i=-1):
		# This function happens after the player decides to split and returns the players last dealt card
		# pop latest from hand 
		return_card =  self.cards.pop(card_i)
		self.ranks.pop(card_i)
		self.suits.pop(card_i)
		self.ids.pop(card_i)
		self.values.pop(card_i)

		# reset the hand identifiers
		self.total = 0 # recalculate
		self.is_soft = False # recalculate
		self.is_bj = False # can not be blackjack
		self.is_buster = False # can not be busted
		self.is_closed = False # can not be closed

		# recalculate total score and if soft of hard hand
		for card in self.cards:
			# calculate total
			if card.rank == 'A':
				self.total += 11
				self.is_soft = True
			else:
				self.total += card.value

		return return_card

	def standHand(self):
		self.is_stand = True
		self.is_closed = True

	def show(self):
		print("In hand: {} \nTotal: {}\nIs a soft hand: {}\nBlackJack: {}\nIs closed: {}\nIs Busted: {}\nIs Stand: {}\n".
				format(self.ids, self.total, self.is_soft, self.is_bj, self.is_closed, self.is_busted, self.is_standed))


	def clear(self):
		self.cards = []
		self.ranks = []
		self.suits = []
		self.ids = []
		self.values = []
		self.total = 0
		self.is_soft = False
		self.is_bj = False
		self.is_busted = False
		self.is_standed = False
		self.is_closed = False



	def __updateHand(self, card):
		self.cards.append(card)
		self.ranks.append(card.rank)
		self.suits.append(card.suit)
		if card.rank == 'A': # append 11 initially and set bool to True
			self.values.append(card.value[1]) 
			self.is_soft = True
		else:
			self.values.append(card.value)
		self.ids.append(card.id)

	def __updateTotal(self, card):
		# update total with card value Ace = 11
		if card.rank == 'A':
			self.total += card.value[1] # =11
		else:
			self.total += card.value

	def __correctForSoftAce(self):
		# if total is over 21 and contains an ace with value 11 set ace to 1 until below 21
		while (self.total > 21 and self.is_soft==True): 
			for i,value in enumerate(self.values): 	# loop over values and find the ace
				if value == 11: 					# if ace is found
					self.values[i] = 1 					# set ace to value of 1
					self.total -= (11-1)				# update total
					break								# break out of forloop only
			if self.__isTwentyOne():				# if 21 set hand to closed and break while
				self.is_closed = True
				
			if self.__isSoft() == False:
				self.is_soft = False

	def __isSoft(self):
		if 11 in self.values:	# if no more Ace with a value of 11 in hand 
			return True 		# is soft
		else:
			return False

	def __isBlackJack(self):
		if self.__isTwentyOne() == True and len(self.cards) == 2:
			return True
		else:
			return False

	def __isTwentyOne(self):
		if self.total == 21:
			return True
		else:
			return False

	def __isBusted(self):
		if self.total > 21:
			return True
		else:
			return False



class Dealer(object):
	def __init__(self, name):
		self.name = name
		self.hand = Hand() # can only have one hand

	def drawCard(self, deck):
		# can draw cards to himself
		self.hand.addCard(deck.drawCard())

	def deal(self, deck):
		# can deal cards to anybody
		return deck.drawCard()



class Player(object):
	def __init__(self, name, bankroll, allowed_splits=1, bet_spread=(1,10)):
		self.name = name
		self.bankroll = bankroll
		self.bet_spread = bet_spread
		self.allowed_splits = allowed_splits
		self.hands = [Hand()] # if player splits person has multiple hands
		self.bets = [0]
		# self.hands = {nr_hands: [] for nr_hands in range(1, allowed_splits+1)}

	def showHands(self):
		for i,hand in enumerate(self.hands):
			print('Hand: {}'.format(i))
			hand.show()

	def showMoney(self):
		print('{} has a bankroll of {} with {} bet(s): {} on the table\n'.format(
								self.name, self.bankroll, len(self.bets), self.bets))

	def bet(self, amount, hand_nr=0):
		print('bet')
		self.__transferMoney(amount, hand_nr)
		# self.bankroll -= amount
		# self.bets.append(amount)

	def hit(self, dealer, deck, hand_nr=0):
		# create check that if hand closet, can not hit
		print('hit')
		card = dealer.deal(deck)
		self.hands[hand_nr].addCard(card)

	def stand(self, hand_nr):
		print('stand')
		self.hands[hand_nr].standHand()

	def dubbleDown(self, dealer, deck, hand_nr=0):
		# create check that if hand closed, can not hit
		# creat check that if contain 2 cards only, can double down
		print('DD')
		self.__transferMoney(self.bets[hand_nr],hand_nr)
		self.hit(dealer, deck, hand_nr)
		# set hand to close as after dubble down it is not possible to hit


	def split(self, hand_nr=0):
		print('split')
		# Get last card from hand you want to split
		split_card = self.hands[hand_nr].splitCard()
		# Create new hand and add card
		self.hands.append(Hand())
		self.hands[hand_nr+1].addCard(split_card)
		# Create similar bet along with this card
		self.bets.append(0) # append new bet field to new hand with 0 money
		self.__transferMoney(self.bets[hand_nr], hand_nr+1) # transfer money to that hand
		# self.bankroll -= self.bets[hand_nr]
		# self.bets.append(self.bets[hand_nr])

	def surrender(self):
		pass

	def __transferMoney(self, amount, hand_nr=0):
		self.bankroll -= amount
		self.bets[hand_nr] += amount


class BlackJack(object):
	def __init__(self, dealer, player_list):
		self.dealer = dealer
		self.player_list = player_list

		

def main():
	deck = Deck(1).shuffle()

	dealer = Dealer('Dealer')
	bob = Player('Bob', 10000, 3)

	# test person class
	ace_of_hearts = Card('A', 'h', (1,11))
	ace_of_diamonds = Card('A', 'd', (1,11))
	king_of_hearts = Card('K', 'h', 10)
	bob.bet(500)
	bob.showMoney()
	bob.hit(dealer, deck)
	bob.hit(dealer, deck)
	bob.showMoney()
	bob.showHands()
	bob.split()
	bob.showHands()
	bob.showMoney()
	bob.dubbleDown(dealer, deck, 0)
	bob.hit(dealer, deck, 1)
	bob.showHands()
	bob.showMoney()



if __name__ == '__main__':
	main()