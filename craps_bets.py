################## Make, Place & Pay Bet Methods for craps-v2.py ###################### 

import linebet

def make_pass_line_bet(self):
	""" Make Pass Line Bet """
	self.pass_line_bet = linebet.LineBet(0, self.min_bet, self.odds_bet, False, True)  # make Pass Line bet with min_bet amount, no odds
	self.table_amount += self.pass_line_bet.get_table_amount()
	self.rail_amount -= self.pass_line_bet.get_table_amount()
	return

def make_dp_line_bet(self):
	""" Make Don't Pass Line Bet """
	self.dp_line_bet = linebet.LineBet(0, self.min_bet, self.odds_bet, False, False)  # make Don't Pass Line bet with min_bet amount, no odds
	self.table_amount += self.dp_line_bet.get_table_amount()
	self.rail_amount -= self.dp_line_bet.get_table_amount()
	return

def make_come_bet(self):
	""" Make Come Line Bet """
	self.come_bets[0] = linebet.LineBet(0, self.min_bet, self.odds_bet, False, True) # Make Come Bet with min_bet amount
	self.rail_amount -= self.come_bets[0].get_table_amount()
	self.table_amount += self.come_bets[0].get_table_amount()
	return

def make_dc_bet(self):
	""" Make Don't Come Line Bet """
	self.dc_bets[0] = linebet.LineBet(0, self.min_bet, self.odds_bet, False, False) # Make Don't Come Bet with min_bet amount
	self.rail_amount -= self.dc_bets[0].get_table_amount()
	self.table_amount += self.dc_bets[0].get_table_amount()
	return

def place_come_bet(self, throw):
	""" Move Placed Come Bet to number """
	if 0 in self.come_bets.keys() and throw in (4, 5, 6, 8, 9, 10):
		del self.come_bets[0]
		self.come_bets[throw] = linebet.LineBet(throw, self.min_bet, self.odds_bet, False, True)
	return

def place_dc_bet(self, throw):
	""" Move Placed Don't Come Bet to number """
	if 0 in self.dc_bets.keys() and throw in (4, 5, 6, 8, 9, 10):
		del self.dc_bets[0]
		self.dc_bets[throw] = linebet.LineBet(throw, self.min_bet, self.odds_bet, False, False)
	return

def place_or_remove_come_bet_odds(self, odds_on, right_way):
	""" Place odds on Come Bets if odds_on = True; otherwise, take Odds off """
	if right_way:
		if odds_on:
			for b in self.come_bets.values():
				if not b.get_odds_on():
					b.put_odds_on()
					self.rail_amount -= b.get_odds_amount()
					self.table_amount += b.get_odds_amount()
		else:
			for b in self.come_bets.values():
				if b.get_odds_on():
					self.rail_amount += b.get_odds_amount()
					self.table_amount -= b.get_odds_amount()
					b.take_odds_off()
		""" Take any odds off any Don't Come Bets if exist """
		for b in self.dc_bets.values():
			if b.get_odds_on():
				self.rail_amount += b.get_odds_amount()
				self.table_amount -= b.get_odds_amount()
				b.take_odds_off()
	else:  # not right_way
		if odds_on:
			for b in self.dc_bets.values():
				if not b.get_odds_on():
					b.put_odds_on()
					self.rail_amount -= b.get_odds_amount()
					self.table_amount += b.get_odds_amount()
		else:
			for b in self.dc_bets.values():
				if b.get_odds_on():
					self.rail_amount += b.get_odds_amount()
					self.table_amount -= b.get_odds_amount()
					b.take_odds_off()
		""" Take any odds off Come Bets if exist """
		for b in self.come_bets.values():
			if b.get_odds_on():
				self.rail_amount += b.get_odds_amount()
				self.table_amount -= b.get_odds_amount()
				b.take_odds_off()
	return

def place_or_remove_pass_bet_odds(self, odds_on, right_way):
	if right_way:
		if odds_on and not self.pass_line_bet.get_odds_on():
			self.pass_line_bet.put_odds_on()
			self.rail_amount -= self.pass_line_bet.get_odds_amount()
			self.table_amount += self.pass_line_bet.get_odds_amount()
		elif not odds_on and self.pass_line_bet.get_odds_on():
			self.rail_amount += self.pass_line_bet.get_odds_amount()
			self.table_amount -= self.pass_line_bet.get_odds_amount()
			self.pass_line_bet.take_odds_off()
	else:  # not right_way
		if odds_on and not self.dp_line_bet.get_odds_on():
			self.dp_line_bet.put_odds_on()  
			self.rail_amount -= self.dp_line_bet.get_odds_amount()
			self.table_amount += self.dp_line_bet.get_odds_amount()
		elif not odds_on and self.dp_line_bet.get_odds_on():
			self.rail_amount += self.dp_line_bet.get_odds_amount()
			self.table_amount -= self.dp_line_bet.get_odds_amount()
			self.dp_line_bet.take_odds_off()
	return

def pay_pass_line_bet(self, is_opening_throw, throw, point):
	""" Update rail_amount & table_amount; return value by which pot_amount component should be incremented"""
	x = 0  # local variable to track winnings/losings
	if is_opening_throw:
		if throw in (7,11):
			""" Win Pass Line Bet """
			self.rail_amount = self.rail_amount + self.pass_line_bet.win_amount() + self.pass_line_bet.get_table_amount()
			self.table_amount -= self.pass_line_bet.get_table_amount()
			x = self.pass_line_bet.win_amount()
		elif throw in (2, 3, 12):
			""" Lose Pass Line Bet """
			self.table_amount -= self.pass_line_bet.lose_amount()
			x = -self.pass_line_bet.lose_amount()
	else:  # is not opening throw
		if throw == point:
			""" Win Pass Line bet """
			self.rail_amount = self.rail_amount + self.pass_line_bet.win_amount() + self.pass_line_bet.get_table_amount()
			self.table_amount -= self.pass_line_bet.get_table_amount()
			x = self.pass_line_bet.win_amount()  
		elif throw == 7:
			""" Lose Pass Line bet """
			self.table_amount -= self.pass_line_bet.lose_amount()
			x = -self.pass_line_bet.lose_amount()
	return x

def pay_dp_line_bet(self, is_opening_throw, throw, point):
	""" Update rail_amount & table_amount; return value by which pot_amount component should be incremented"""
	x = 0  # local variable to track winnings/losings
	if is_opening_throw:
		if throw in (7,11):
			""" Lose Don't Pass Line bet """
			self.table_amount -= self.dp_line_bet.lose_amount()
			x = -self.dp_line_bet.lose_amount()
		elif throw in (2,3):
			""" Win Don't Pass Line bet """
			self.rail_amount = self.rail_amount + self.dp_line_bet.win_amount() + self.dp_line_bet.get_table_amount()
			self.table_amount -= self.dp_line_bet.get_table_amount()
			x = self.dp_line_bet.win_amount()
		elif throw == 12:
			""" Push Don't Pass Line Bet """
			self.rail_amount += self.dp_line_bet.get_table_amount()
			self.table_amount -= self.dp_line_bet.get_table_amount()
	else:  # is not opening throw
		if throw == point:
			""" Lose Don't Pass Line bet """
			self.table_amount -= self.dp_line_bet.get_table_amount()
			x = -self.dp_line_bet.lose_amount() # Don't Pass Line loses
		elif throw == 7:
			""" Win Don't Pass Line bet """
			self.rail_amount = self.rail_amount + self.dp_line_bet.win_amount() + self.dp_line_bet.get_table_amount()
			self.table_amount -= self.dp_line_bet.get_table_amount()
			x = self.dp_line_bet.win_amount() # Don't Pass Line wins
	return x

def pay_come_bets(self, throw):
	""" Update rail_amount & table_amount; return value by which pot_amount component should be incremented"""
	x = 0  # local variable to track winnings/losings
	if throw == 7:
		""" Win Made Come Bet then Delete """ 
		if 0 in self.come_bets.keys():
			x += self.come_bets[0].win_amount()
			self.rail_amount = self.rail_amount + self.come_bets[0].win_amount() + self.come_bets[0].get_table_amount()
			self.table_amount -= self.come_bets[0].get_table_amount()
			del self.come_bets[0]
		""" Lose all Come Line bets """
		for b in self.come_bets.values():
			x -= b.lose_amount()
			self.table_amount -= b.lose_amount()
		""" Delete all Placed Come Bets """ 
		self.come_bets.clear()

	elif throw in (4, 5, 6, 8, 9, 10):
		if throw in self.come_bets.keys():
			""" Win Come Line bet and delete it"""
			self.rail_amount = self.rail_amount + self.come_bets[throw].get_table_amount() + self.come_bets[throw].win_amount()
			self.table_amount -= self.come_bets[throw].get_table_amount()
			x = self.come_bets[throw].win_amount()
			del self.come_bets[throw]
	elif throw in (2, 3, 11, 12):
		if 0 in self.come_bets.keys():
			if throw in (2, 3, 12):
				""" Lose Made Come Bet """
				x -= self.come_bets[0].lose_amount()
				self.table_amount -= self.come_bets[0].get_table_amount()
			elif throw == 11:
				""" Win Made Come Bet """
				x += self.come_bets[0].win_amount()
				self.rail_amount = self.rail_amount + self.come_bets[0].win_amount() + self.come_bets[0].get_table_amount()
				self.table_amount -= self.come_bets[0].get_table_amount()
			""" Delete Made Come Bet """
			del self.come_bets[0]
	return x

def pay_dc_bets(self, throw):
	""" Update rail_amount & table_amount; return value by which pot_amount component should be incremented"""
	x = 0  # local variable to track winnings/losings
	if throw == 7:
		""" Lose Made Come Bet then Delete """
		if 0 in self.dc_bets.keys():
			x -= self.dc_bets[0].lose_amount()
			self.table_amount -= self.dc_bets[0].get_table_amount()
			del self.dc_bets[0]
		""" Win all Don't Come Bets """
		for b in self.dc_bets.values():  # Pay all Don't Come Line bets w/ any Don't Come Odds
			x += b.win_amount()
			self.rail_amount = self.rail_amount + b.win_amount() + b.get_table_amount()
			self.table_amount = self.table_amount - b.get_table_amount()
		""" Delete all Placed Come Bets"""
		self.dc_bets.clear()
	elif throw in (4, 5, 6, 8, 9, 10):
		if throw in self.dc_bets.keys():
			""" Lose Don't Come Line Bet and delete it """
			self.table_amount -= self.dc_bets[throw].lose_amount()
			x = -self.dc_bets[throw].lose_amount()
			del self.dc_bets[throw]
	elif throw in (2, 3, 11, 12):
		if 0 in self.dc_bets.keys():
			if throw in (2, 3):
				""" Win Made Don't Come Bet """
				x += self.dc_bets[0].win_amount()
				self.rail_amount = self.rail_amount + self.dc_bets[0].win_amount() + self.dc_bets[0].get_table_amount()
				self.table_amount -= self.dc_bets[0].get_table_amount()
			elif throw == 11:
				""" Lose Made Don't Come Bet """
				x -= self.dc_bets[0].lose_amount()
				self.table_amount -= self.dc_bets[0].lose_amount()
			elif throw == 12:
				""" Push Made Don't Come Bet """
				self.rail_amount += self.dc_bets[0].get_table_amount()
				self.table_amount -= self.dc_bets[0].get_table_amount()
			del self.dc_bets[0]
	return x