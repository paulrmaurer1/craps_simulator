################### Print Methods for craps-v2.py ######################

def print_pre_opening_roll_bets(self):
	print ('########### Pre-opening Roll Bets ##########')
	if self.odds_on[0]:
		print ('Odds are currently ON; # rolls since changed to ON: {}'.format(str(self.odds_on[1])))
	else:
		print ('Odds are currently OFF; # rolls since change to OFF: {}'.format(str(self.odds_on[1])))
	print ('  Pass Line bet is ON: ${}  |  Don\'t Pass Line bet is ON: ${}'.\
		format(str(self.pass_line_bet.get_bet_amount()), str(self.dp_line_bet.get_bet_amount())))
	if self.come_bets.values() or self.dc_bets.values():
		print ('Come/Don\'t Come Bets existing (from last shooter_roll) on Come Out roll')
		for b in self.come_bets.values():
			print (str(b))
		for b in self.dc_bets.values():
			print (str(b))
	print ('Pot Amount: ${} | Rail Amount: ${} | Table Amount: ${}'.format(str(self.pot_amount), str(self.rail_amount), str(self.table_amount)))
	return

def print_pre_roll_bets(self):
	print ('########### Pre-Roll Bets ##########')
	if self.odds_on[0]:
		print ('Odds are currently ON; # rolls since changed to ON: {}'.format(str(self.odds_on[1])))
	else:
		print ('Odds are currently OFF; # rolls since changed to OFF: {}'.format(str(self.odds_on[1])))
	print ('  Pass Line({}): ${}  Odds: ${}'.\
			format(str(self.pass_line_bet.get_point()), str(self.pass_line_bet.get_bet_amount()), \
				str(self.pass_line_bet.get_odds_amount())))
	print ('  Don\'t Pass Line({}): ${}  Odds: ${}'.\
			format(str(self.dp_line_bet.get_point()), str(self.dp_line_bet.get_bet_amount()), \
				str(self.dp_line_bet.get_odds_amount())))
	if 0 in self.come_bets.keys():
		come_bet_status = '  Come bet is ON: ${}'.format(str(self.come_bets[0].get_table_amount()))
	else:
		come_bet_status =  '  Come bet is OFF'
	if 0 in self.dc_bets.keys():
		dc_bet_status =  '  Don\'t Come bet is ON: ${}'.format(str(self.dc_bets[0].get_table_amount()))
	else:
		dc_bet_status =  '  Dont\'t Come bet is OFF'
	print (come_bet_status + ' |' + dc_bet_status)
	for b in self.come_bets.values():
		if b.get_point() != 0:
			print (str(b))
	for b in self.dc_bets.values():
		if b.get_point() != 0:
			print (str(b))
	print ('Pot Amount: ${} | Rail Amount: ${} | Table Amount: ${}'.format(str(self.pot_amount), str(self.rail_amount), str(self.table_amount)))
	print ()
	return

def print_ending_positions(self):
	""" Print ending Class variables """
	print ('Pot Amount: ${} | Rail Amount: ${} | Table Amount: ${}'.format(str(self.pot_amount), str(self.rail_amount), str(self.table_amount)))
	for b in self.come_bets.values():
		if b.get_point() != 0:
			print (str(b))
	for b in self.dc_bets.values():
		if b.get_point() != 0:
			print (str(b))
	print()
	return