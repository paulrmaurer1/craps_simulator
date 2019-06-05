import craps_methods

#This file contains objects and methods needed to mode a Come or Don't Come bet and will be called
#by the craps.py module

class LineBet(object):
	def __init__(self, point, line_bet, odds_bet, odds_on, right_way):
		"""
		LineBet is class object used to track Pass/Don't Pass Line or Come/Don't Come Line bets
		point is the number (4, 5, 6, 8, 9, 10) that a bet represents
		line_bet is $ amount bet on Pass/Don't Pass Line or Come/Don't Come Line
		odds_bet is the $ odds amount set for betting (e.g. $10 behind line), not the actual odds amount laid
		odds_on is True/False indicating if Odds are on or not
		right_way is a boolean indicating whether object represents a Pass/Come (True) bet or Don't Pass/Don't Come (False) bet
		odds_amount is the current amount of actual Odds laid on a bet (if right_way = False, this is the amount needed to win self.odds_bet)
		"""
		self.point = point
		self.line_bet = line_bet
		self.odds_bet = odds_bet
		self.odds_on = odds_on
		self.right_way = right_way
		self.point_thrown = False
		if odds_on:
			self.odds_amount = craps_methods.placeOdds(self.point, self.odds_bet, self.right_way)
		else:
			self.odds_amount = 0

	def get_point(self):
		return self.point

	def set_point(self, point):
		self.point = point
		self.point_thrown = True
		return

	def win_amount(self):
		return self.line_bet + craps_methods.payOdds(self.point, self.odds_amount, self.right_way)
		
	def lose_amount(self):
		return self.line_bet + self.odds_amount
		
	def put_odds_on(self):
		self.odds_on = True
		self.odds_amount = craps_methods.placeOdds(self.point, self.odds_bet, self.right_way)
		return

	def take_odds_off(self):
		self.odds_on = False
		self.odds_amount = 0
		return

	def get_odds_on(self):
		return self.odds_on

	def get_right_way(self):
		return self.right_way

	def get_bet_amount(self):
		return self.line_bet

	def get_odds_amount(self):
		return self.odds_amount

	def get_table_amount(self):
		return self.line_bet + self.odds_amount

	def __str__(self):
		if self.right_way:
			return '     Come Bet({}): ${}  Odds: ${}'.format(str(self.point), str(self.line_bet), str(self.odds_amount))
		else:
			return '     Don\'t Come Bet({}): ${}  Odds: ${}'.format(str(self.point), str(self.line_bet), str(self.odds_amount))