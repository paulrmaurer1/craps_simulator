import random, numpy, craps_plot, craps_v2

def crapsTestSim_v2(numRolls):
	"""Plays numRolls consecutive shooter_rolls for testing purposes"""
	minimum_bet = 5  # Minimium bet to place on the Pass/Don't Pass & Come/Don't Come lines
	odds_bet = 10  # Odds bet to place behind the Pass/Don't Pass & Come/Don't Come lines
	starting_pot = 300  # Starting amount with which to bet
	right_way = True  # True = bet "Do"/Pass/Come side; False = bet "Don't" Pass/Come side
	print_results = True  # Print results of each roll; good to use while testing

	c = craps_v2.CrapsGame(minimum_bet, odds_bet, starting_pot, print_results)

	for t in range(numRolls):
		c.shooter_rolls(right_way)

def crapsTestSim_v3(numSessions):
	"""Play numSessions sessions.  Each session consists of x shooter rolls until either the pot_low or pot_high amount is reached"""
	minimum_bet = 5  # Minimium bet to place on the Pass/Don't Pass & Come/Don't Come lines
	odds_bet = 10  # Odds bet to place behind the Pass/Don't Pass & Come/Don't Come lines
	starting_pot = 300  # Starting amount with which to bet
	right_way = False  # True = bet "Do"/Pass/Come side; False = bet "Don't" Pass/Come side
	print_results = True  # Print results of each roll; good to use while testing
	walk_away_pot_low = 150  # Pot amount under which walk away from table, i.e. end of session
	walk_away_pot_high = 450  # Pot amount above which walk away from table, i.e. end of session
	
	for t in range(numSessions):
		num_shooters = 0
		c = craps_v2.CrapsGame(minimum_bet, odds_bet, starting_pot, print_results)
		pot_tracker = []
		roll_tracker = []
		while c.potamountleft() > walk_away_pot_low and c.potamountleft() < walk_away_pot_high:
			""" 
			Ensure that finish a shooter turn to completion, i.e. craps out, before evaluating pot_amount
			So that there are no Come or Don't Come Bets left on the table
			"""
			while c.get_point_crapped() == False and c.potamountleft() > walk_away_pot_low and c.potamountleft() < walk_away_pot_high:
				c.shooter_rolls(right_way)
			c.reset_point_crapped()
			num_shooters += 1

		print('Session #{}: # Shooters = {}, Ending Pot Amount = ${}'.format(t+1, num_shooters, c.potamountleft()))
	

def crapsSessionSim_v2(numSessions):
	"""Play numSessions sessions.  Each session consists of x shooter rolls until either the pot_low or pot_high amount is reached"""
	games_won, games_lost = [], []
	pot_when_win, pot_when_lose = [], []
	shooters_when_win, shooters_when_lose = [], []
	num_come_bets_left, amount_come_bets_left = [], []
	shooter_pot_values = []  # a list containing each session's (list of) ending pot values (stored in pot_tracker below) - the y values for plotting
	shooter_roll_values = []  # a list containing each session's (list of) rolls - the x values for plotting
	
	
	minimum_bet = 5  # Minimium bet to place on the Pass/Don't Pass & Come/Don't Come lines
	odds_bet = 10  # Odds bet to place behind the Pass/Don't Pass & Come/Don't Come lines
	starting_pot = 300  # Starting amount with which to bet
	right_way = False  # True = bet "Do"/Pass/Come side; False = bet "Don't" Pass/Come side
	print_results = False  # Print results of each roll; good to use while testing
	plot_results = True # Plot results of each session in pylab
	walk_away_pot_low = 150  # Pot amount under which walk away from table, i.e. end of session
	walk_away_pot_high = 450  # Pot amount above which walk away from table, i.e. end of session
	
	num_wins = 0
	
	for t in range(numSessions):
		num_shooters = 0
		c = craps_v2.CrapsGame(minimum_bet, odds_bet, starting_pot, print_results)
		pot_tracker = []
		roll_tracker = []
		while c.potamountleft() > walk_away_pot_low and c.potamountleft() < walk_away_pot_high:
			""" 
			Ensure that finish a shooter turn to completion, i.e. craps out, before evaluating pot_amount
			So that there are no Come or Don't Come Bets left on the table
			"""
			while c.get_point_crapped() == False and c.potamountleft() > walk_away_pot_low and c.potamountleft() < walk_away_pot_high:
				c.shooter_rolls(right_way)
			c.reset_point_crapped()
			num_shooters += 1

			if plot_results:
				pot_tracker.append(c.potamountleft())
				roll_tracker.append(num_shooters)
		# print ('Session #: {} completed..'.format(t+1))

		if c.potamountleft() >= walk_away_pot_high:
			num_wins += 1
			shooters_when_win.append(num_shooters)
			games_won.append(c)
		else:
			shooters_when_lose.append(num_shooters)
			games_lost.append(c)
		
		if plot_results:
			shooter_pot_values.append(pot_tracker)
			shooter_roll_values.append(roll_tracker)
		
	"""Generate ending pot statistics for each session"""
	for g in games_won:
		pot_when_win.append(g.potamountleft())
	for g in games_lost:
		pot_when_lose.append(g.potamountleft())

	winning_perc = str(round(100*num_wins/numSessions, 2)) + '%'
	if num_wins != 0:
		avg_num_shooters_win = str(round(sum(shooters_when_win)/num_wins, 1))
		avg_pot_when_win = str(round(sum(pot_when_win)/num_wins, 2))
	else:
		avg_num_shooters_win = str(0)
		avg_pot_when_win = str(0)

	avg_num_shooters_lose = str(round(sum(shooters_when_lose)/(numSessions-num_wins), 1))
	avg_pot_when_lose = str(round(sum(pot_when_lose)/(numSessions-num_wins), 2))
	# avg_come_bets_left = str(round(sum(num_come_bets_left)/len(num_come_bets_left), 1))
	# avg_come_bets_amounts = str(round(sum(amount_come_bets_left)/len(amount_come_bets_left), 2))
	# avg_times_points_thrown = str(round(100*len(num_come_bets_left)/(sum(shooters_when_win)+sum(shooters_when_lose)), 1)) + '%'


	if plot_results:
		max_pot = max(pot_when_win)
		# min_pot = min(pot_when_lose)
		min_pot = 0
		max_rolls = max(max(shooters_when_win), max(shooters_when_lose))
		craps_plot.plot_sessions(shooter_pot_values, shooter_roll_values, max_pot, min_pot, max_rolls)

	print ('Out of', str(numSessions), 'Craps sessions played:')
	print ('With a starting pot of $', str(starting_pot),' Betting Do/Pass line: ', str(right_way))
	print ('And a walk-away pot between $', str(walk_away_pot_low), ' and $', str(walk_away_pot_high))
	print ('   Winning percentage is : {}  # Wins: {}   # Losses: {}'.format(winning_perc, num_wins, numSessions-num_wins))
	print ('   Average number of shooters per game (when win) is: ', avg_num_shooters_win, ' Avg pot after win = $', avg_pot_when_win)
	print ('   Average number of shooters per game (when lose) is: ', avg_num_shooters_lose, ' Avg pot after loss = $', avg_pot_when_lose)
	# print ('   Average Come bets left after point thrown is: ', avg_come_bets_left, 'Avg Come bets $$ after point thrown = $', avg_come_bets_amounts)
	# print ('   Avg shooter rolls that point is thrown is: ', avg_times_points_thrown)

def crapsRoiSim_v2(numSessions):
	"""Play numShooters sessions. Each session ends when a Shooter craps out, i.e. rolls 7, after having established a point"""
	ROIPerShooter = []
	EndingPotAmount = []
	NumberShooters = []

	minimum_bet = 5  # Minimium bet to place on the Pass/Don't Pass & Come/Don't Come lines
	odds_bet = 10  # Odds bet to place behind the Pass/Don't Pass & Come/Don't Come lines
	starting_pot = 300  # Starting amount with which to bet
	right_way = True  # True = bet "Do"/Pass/Come side; False = bet "Don't" Pass/Come side
	print_results = False  # Print results of each roll; good to use while testing
	num_points_crapped = 5  # The number of crap out events a player stays at the table

	for t in range(numSessions):
		num_shooters = 0
		c = craps_v2.CrapsGame(minimum_bet, odds_bet, starting_pot, print_results)
		for u in range(num_points_crapped):
			while c.get_point_crapped() == False:
				c.shooter_rolls(right_way)
				num_shooters += 1
				# print ('Shooter_rolls event #:{}'.format(num_shooters))
			c.reset_point_crapped()

		ROIPerShooter.append((c.potamountleft()-starting_pot)/starting_pot)
		EndingPotAmount.append(c.potamountleft())
		NumberShooters.append(num_shooters)
		# print ('Pot Amount at end of Shooter #{} session: ${}  # shooter_rolls: {}'.format(t+1, c.potamountleft(), num_shooters))

	meanROI = str(round(100*numpy.average(ROIPerShooter), 4)) + '%'
	ROI_sigma = str(round(100*numpy.std(ROIPerShooter), 4)) + '%'
	meanEndingPotAmount = str(round(numpy.average(EndingPotAmount), 2))
	EndingPotAmount_sigma = str(round(numpy.std(EndingPotAmount), 2))
	AvgNumberShooters = str(round(numpy.average(NumberShooters),1))
	
	print('For {} Sessions, Average Ending Pot Amount = ${} Pot Amount Std. Dev. = ${}'.format(numSessions, meanEndingPotAmount, EndingPotAmount_sigma))
	print('  Mean ROI = {}  ROI Std. Dev. = {}'.format(meanROI, ROI_sigma))
	print('  Average # shooters per session = {}'.format(AvgNumberShooters))

def crapsRoiSim_v3(numSimulations):
	"""Based on a set number of Simulations, run an increasing # of sessions* and determine STD of ending pot amount"""
	"""   *session ends when a Shooter craps out after having established a point """
	AvgEndingPotAmount = []
	HighEndingPotAmount = [] # 2 standard deviations above average, i.e. upper bound of 95%
	LowEndingPotAmount = [] # 2 standard deviations below average, i.e. lower bound of 95%
	NumberSessions = [] # Number of sessions played, x-axis

	minimum_bet = 5  # Minimium bet to place on the Pass/Don't Pass & Come/Don't Come lines
	odds_bet = 10  # Odds bet to place behind the Pass/Don't Pass & Come/Don't Come lines
	starting_pot = 300  # Starting amount with which to bet
	right_way = True  # True = bet "Do"/Pass/Come side; False = bet "Don't" Pass/Come side
	print_results = False  # Print results of each roll; good to use while testing

	for y in range(5, 50, 5):
		NumberSessions.append(y)
		EndingPotAmount = []
		for x in range(numSimulations):
			for t in range(y):
				c = craps_v2.CrapsGame(minimum_bet, odds_bet, starting_pot, print_results)
				while c.get_point_crapped() == False:
					c.shooter_rolls(right_way)
				EndingPotAmount.append(c.potamountleft())
		
		AvgPotAmount = round(numpy.average(EndingPotAmount),2)
		AvgEndingPotAmount.append(AvgPotAmount)
		HighEndingPotAmount.append(round(AvgPotAmount + 2 * numpy.std(EndingPotAmount), 2))
		LowEndingPotAmount.append(round(AvgPotAmount - 2 * numpy.std(EndingPotAmount), 2))

	print(AvgEndingPotAmount)
	print(HighEndingPotAmount)
	print(LowEndingPotAmount)
	print(NumberSessions)


# Uncomment module that should be executed when 'python craps_sim.py' is run from the command line

#crapsTestSim_v2(3)
# crapsTestSim_v3(1)

crapsSessionSim_v2(1000)

#crapsRoiSim_v2(1000)
#crapsRoiSim_v3(10)