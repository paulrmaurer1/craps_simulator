import linebet, craps_methods

"""
This file contains the CrapsGame object and methods needed to simulate a craps game whereby the minimum
betting amount is placed on both the pass line and don't pass line and subsequent bets can
either be made on the Do (right_way) or Don't (cold) side of the Pass/Come Lines
"""
class CrapsGame(object):
	def __init__(self, min_bet, odds_bet, start_amount, print_results):
		"""Passed variables"""
		self.min_bet = min_bet  # amount bet (int) on pass/don't pass line, come/don't come line
		self.odds_bet = odds_bet  # amount (int) that can be bet "behind the pass/don't pass or come/don't come line"
		self.start_amount = start_amount  # $ amount with which one walks up to table
		self.print_results = print_results # True/False whether to pring roll by roll stats (for testing)
		"""CrapsGame strategy settings"""
		self.max_num_come_bets = 3  # maximum # Come Line bets
		self.max_num_dc_bets = 3  # maximum # Don't Come Line bets
		self.num_consec_clean_throws_place_odds = 3  # number of non-craps throws before placing Come Odds bets
		self.num_consec_nowin_throws_remove_odds = 2  # number of non-win throws before removing Come Odds bets
		"""Bets that can be placed within a CrapsGame"""
		self.pass_line_bet = None  # placeholder for Pass Line bet
		self.dp_line_bet = None  # placeholder for Don't Pass Line bet
		self.come_bets = {}  # dict of point:LineBet objects to track Come Line bets that are still active after shooter roll
		self.dc_bets = {}  # dict of point:LineBet objects to track Don't Come Line bets that are still active after shooter roll
		"""Tracking variables applicable across many shooter_rolls events"""
		self.table_amount = 0  # track $$ physically on table during shooter roll
		self.rail_amount = start_amount # track $$ physically in rail during shooter roll
		self.pot_amount = start_amount # track total $$ won/lost including amount on table during shooter roll
		self.odds_on = [False, 0] # [True/False: # rolls @ current status] to track when to place Odds bets on Pass/Don't Pass & Come/Don't Come bets
		"""Craps_sim.py variables needed to determine when to end simulation and track statistics """
		self.point_thrown = False  # track whether once a point is established, the point was thrown before 7
		self.point_crapped = False  # track whether once a point is established, shooter crapped
		
	#Imported class methods
	from craps_bets import make_pass_line_bet, make_dp_line_bet, make_come_bet, make_dc_bet, \
		place_come_bet, place_dc_bet, place_or_remove_come_bet_odds, place_or_remove_pass_bet_odds, \
		pay_pass_line_bet, pay_dp_line_bet, pay_come_bets, pay_dc_bets
	from print_methods import print_pre_opening_roll_bets, print_pre_roll_bets, print_ending_positions
		
	def shooter_rolls(self, right_way):
		"""
		Each shooter_rolls function ends when either a 7/11 or 2/3/12 is thrown on first roll
		or point is established then thrown again or crapped (i.e. roll 7)
		New pass line and don't pass line bets are made during each shooter_rolls function
		"""

		"""Shooter Roll counters &  tracking variables"""
		pass_win_amount, dp_win_amount, come_win_amount, dc_win_amount = 0, 0, 0, 0 # self.pot_amount component variables
		shooter_roll_start_amount = self.pot_amount
		is_opening_throw = True
		num_throws_clean = 0  # Track # clean rolls during shooter_rolls event
		
		########################################################################
		###################### MAKE OPENING BETS ###############################
		########################################################################
				
		""" Place or remove odds on Come & Don't Come Bets based on odds_on[0] if exist from prior shooter_rolls """
		self.place_or_remove_come_bet_odds(self.odds_on[0], right_way)
		
		""" Check to ensure have enough $$ to place initial bets then place initial bets """
		if self.rail_amount < (2 * self.min_bet):  
			pass # If don't have enough to place min bet on Pass & Don't Pass Line, don't bet, pass
		else:
			""" Make Pass Line Bet """
			self.make_pass_line_bet()
			""" Make Don't Pass Line Bet """
			self.make_dp_line_bet()
		
		""" Print pre-opening Roll Bet positions """
		if self.print_results:
			self.print_pre_opening_roll_bets()

		##############################################################################################
		############################## THROW OPENING ROLL & PAY BETS #################################
		##############################################################################################
		opening_throw = craps_methods.rollDie() + craps_methods.rollDie()
		num_throws_clean += 1  # After opening roll, incremement # clean throws
		self.odds_on[1] += 1  # After opening roll, increment # throws at current odds status

		""" Print Opening Roll result """ 
		if self.print_results:
			print ()
			print ('**********************************')
			print ('*OPENING ROLL: ******** {} ********'.format(str(opening_throw)))
			print ('**********************************')
			print ()
		

		""" Update odds strategy based on opening roll """
		self.update_odds_for_next_throw(right_way, is_opening_throw, opening_throw, 0)

		""" Pay active bets and update shooter_roll counters """
		pass_win_amount += self.pay_pass_line_bet(is_opening_throw, opening_throw, 0)
		dp_win_amount += self.pay_dp_line_bet(is_opening_throw, opening_throw, 0)
		come_win_amount += self.pay_come_bets(opening_throw)
		dc_win_amount += self.pay_dc_bets(opening_throw)

		if opening_throw in (4, 5, 6, 8, 9, 10):
			#############################################################################################
			#################################### POINT THROWN ###########################################
			#############################################################################################
			point = opening_throw
			self.pass_line_bet.set_point(point) # Set Pass Line bet point to Opening Throw
			self.dp_line_bet.set_point(point)  # Set Don't Pass Line bet point to Opening Throw
			
			""" Print post-opening Roll Come Bet stats """
			if self.print_results and (self.come_bets.values() or self.dc_bets.values()):
				print ('--------------- From Opening Roll -------------------------')
				print ('  Come Line win: ${}  Don\'t Come Line win: ${}'.format(str(come_win_amount), str(dc_win_amount)))
				print ('----------------------------------------------------------')
				print ()
							
			#################################################################################################			
			"""Once point is thrown, keep rolling and increase/decrease bets as num_throws increases"""

			while True:

				""" Lay Odds on Come Bets or Don't Come Bets if self.odds_on[0] is True, otherwise, remove before next roll """
				self.place_or_remove_come_bet_odds(self.odds_on[0], right_way)

				"""  Lay Odds on Pass and Don't Pass Line bets if self.odds_on[0] is True, otherwise, remove before next roll """
				self.place_or_remove_pass_bet_odds(self.odds_on[0], right_way)
				
				""" Place Come & Don't Come bets if applicable """
				if len(self.come_bets) < self.max_num_come_bets:
					self.make_come_bet()

				if len(self.dc_bets) < self.max_num_dc_bets:
					self.make_dc_bet()

				"""Print pre-roll betting lines and amounts"""
				if self.print_results:
					self.print_pre_roll_bets()

				####################################################################################################
				################################ THROW NEXT ROLL & PAY/PLACE BETS ##################################
				####################################################################################################

				throw = craps_methods.rollDie() + craps_methods.rollDie()
				is_opening_throw = False
				num_throws_clean += 1   # track overall # of clean throws, i.e. not a 7 or point, for printing purposes
				self.odds_on[1] += 1   # Increment odds_on roll count for odds strategy
				

				if self.print_results:
					# input ('When ready to roll, hit RETURN..')
					print ()
					print ('**************************************')
					print ('*...Clean Roll #{}: ******** {} ********'.format(str(num_throws_clean),str(throw)))
					print ('**************************************')
					print ()

				""" 
				Update Odds for next dice throw. Important to do this before payouts
				since self.pay_come_bets() and self.pay_dc_bets() deletes Come Bet after paying
				"""
				self.update_odds_for_next_throw(right_way, is_opening_throw, throw, point)

				
				""" Settle Up Pass Line bet """
				pass_win_amount += self.pay_pass_line_bet(is_opening_throw, throw, point)

				""" Settle Up Don't Pass Line bet """
				dp_win_amount += self.pay_dp_line_bet(is_opening_throw, throw, point)
				
				""" Settle Up Come Bets """
				come_win_amount += self.pay_come_bets(throw)
				
				""" Settle Up Don't Come Bets """
				dc_win_amount += self.pay_dc_bets(throw)
				
				
				""" Place Come/Don't Come Line bets on number thrown if Come/Don't Come bet made prior to roll """
				if 0 in self.come_bets.keys():
					self.place_come_bet(throw)
				if 0 in self.dc_bets.keys():
					self.place_dc_bet(throw)
				
				# Break out of while loop if throw 7 or hit point, update variable
				if throw == point:  # hit number :)
					self.point_thrown = True
					break
								
				elif throw == 7:  # roll Craps :(  
					self.point_crapped = True
					break

				""" Update self.pot_amount for next pre-roll stats """
				self.pot_amount = shooter_roll_start_amount + pass_win_amount + dp_win_amount + come_win_amount + dc_win_amount

				if self.print_results:
					print ('--------- Come Line / Don\'t Come Line Update ---------')
					print ('  Come Line win: ${}  Don\'t Come Line win: ${}'.format(str(come_win_amount), str(dc_win_amount)))
					print ('----------------------------------------------------------')
		
		
		########################################################################
		#################### END OF ROLL STATISTICS ############################
		########################################################################

		self.pot_amount = shooter_roll_start_amount + pass_win_amount + dp_win_amount + come_win_amount + dc_win_amount
		
		if self.print_results:
			print ('########### Ending Positions ##########')
			print ('Shooter Win/Loss: ${} | Pass Line win: ${} | DP Line win: ${} | Come Line win: ${} | Don\'t Come Line win: ${}'\
				.format(str(pass_win_amount + dp_win_amount + come_win_amount + dc_win_amount), \
				str(pass_win_amount), str(dp_win_amount), str(come_win_amount), str(dc_win_amount)))
			self.print_ending_positions()
		
		return	

	########################################################################
	####################### CrapsGame METHODS ##############################
	########################################################################

	######## These methods determine odds strategy #########################
	def update_odds_for_next_throw(self, right_way, is_opening_throw, throw, point):
		""" 
		This strategy put odds on Come/Don't Come Bets & Pass/Don't Pass Line bets if the 
		previous roll wins on any Come/Don't Come Bet or Pass/Don't Pass Line bet; 
		otherwise, takes odds off if loses on previous roll (depending on right_way). Lastly,
		checks to see if rolls since odds switched have reached thresholds set by strategy
		"""
		if throw == point:
			if right_way:
				""" If hit number, place odds on Come Bets on next opening shooter_roll """
				self.odds_on = [True, 0]
				return
			else:
				""" If hit number, remove odds on Don't Come Bets on next opening shooter_roll """
				# self.odds_on = [False, 0]
				""" Always have Don't Come Bets odds on """
				self.odds_on = [True, 0] 
				return

		elif throw == 7 and not is_opening_throw:
			if right_way:
				""" If crap out, remove Come Bet odds on next opening shooter_roll """
				self.odds_on = [False, 0]
				return
			else:
				""" If crap out, remove Don't Come Bet odds on next opening shooter_roll """
				self.odds_on = [True, 0]
				return
		
		elif throw in (4, 5, 6, 8, 9, 10):
			if right_way:
				if throw in self.come_bets.keys():
					""" If hit Come Bet #, then put odds on all Come Bets """
					self.odds_on = [True, 0]
					return
			else:
				if throw in self.dc_bets.keys():
					""" If hit Don't Come Bet #, then take odds off all Don't Come Bets """
					# self.odds_on = [False, 0]
					""" Always have Don't Come Bets odds on """
					self.odds_on = [True, 0] 
					return

		""" After applying above rules, check number of rolls, i.e. self.odds_on[1] to see if threshold reached since switching odds """
		if right_way:
			if (not self.odds_on[0] and self.odds_on[1] >= self.num_consec_clean_throws_place_odds):
				""" place Odds after 'self.num_consec_clean_throws_place_odds' clean rolls with Odds not on or Come Bet/Pass Line Line win """
				self.odds_on = [True, 0]
			elif self.odds_on[0] and self.odds_on[1] >= self.num_consec_nowin_throws_remove_odds:
				""" remove Odds after 'self.num_consec_nowin_throws_remove_odds' rolls without a Come Bet Line win """
				self.odds_on = [False, 0]

			####### TO ALWAYS HAVE ODDS_ON DURING RIGHT WAY, UNCOMMENT BELOW #####
			# self.odds_on[0] = True
		else:
			######### TO USE WRONG WAY COUNTERS, UNCOMMENT THE BELOW SECTION #######
			# if (not self.odds_on[0] and self.odds_on[1] >= self.num_consec_clean_throws_place_odds):
			# 	""" place Odds after 'self.num_consec_clean_throws_place_odds' clean rolls with Odds not on """
			# 	self.odds_on = [True, 0]
			# elif self.odds_on[0] and self.odds_on[1] >= self.num_consec_nowin_throws_remove_odds:
			# 	""" remove Odds after 'self.num_consec_nowin_throws_remove_odds' rolls without a Come Bet Line win or Don't Come Bet/Don't Pass Line loses """
			# 	self.odds_on = [False, 0]
			
			######### TO ALWAYS HAVE ODDS_ON DURING WRONG WAY, UNCOMMENT BELOW #####
			self.odds_on[0] = True
		return

	
	######## These methods used by craps_sim.py to gather stats and gauge when to stop running simulation ######
	def potamountleft(self):
		return self.pot_amount

	def get_point_thrown(self):
		return self.point_thrown

	def get_point_crapped(self):
		return self.point_crapped

	def reset_point_crapped(self):
		self.point_crapped = False
		return

	def get_oddsbets_totals(self):
		""" Returns total Odds placed on Come Line & Don't Come Line bets """
		come_bets_total, dc_bets_total = 0, 0
		for b in self.come_bets.values():
			come_bets_total += b.get_odds_amount()
		for b in self.dc_bets.values():
			dc_bets_total += b.get_odds_amount()
		return max (come_bets_total, dc_bets_total)

	def get_num_oddsbets(self):
		""" Returns dicts with Come/Don't Come Line #s & Odds bets (assumption is the min_bet is on Come Line) """
		come_bets_num, dc_bets_num = 0, 0
		for b in self.come_bets.keys():
			come_bets_num += 1
		for b in self.dc_bets.keys():
			dc_bets_num += 1
		return max (come_bets_num, dc_bets_num)