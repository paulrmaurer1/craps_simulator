import random

def rollDie():
	return random.choice([1,2,3,4,5,6])

def payOdds(num, bet, right_way):
	"""
	num is 4, 5, 6, 8, 9, or 10, i.e. possible points on which a pass, don't pass, come or don't come bet Odds are paid
	bet is what was placed behind the pass, don't pass, come or don't come line
	right_way is boolean indicating if betting Pass/Come (True) or Don't Pass/Come (False) side of point
	"""
	if bet == 0 or num not in (4, 5, 6, 8, 9, 10):
		return 0
	if right_way:
		if num == 4 or num == 10:
			return int(bet * 2)  # e.g. pay $20 on $10
		elif num == 5 or num == 9:
			return int(bet * 3 / 2)  # e.g. pay $15 on $10
		elif num == 6 or num == 8:
			return int(bet * 6 / 5)  # e.g. pay $12 on $10
	else:
		if num == 4 or num == 10:
			return int(bet / 2)  # e.g. pay $10 on $20
		elif num == 5 or num == 9:
			return int(bet * 2 / 3)  # e.g. pay $10 on $15
		elif num == 6 or num == 8:
			return int(bet * 5 / 6)   # e.g. pay $10 on $12

def placeOdds(num, bet, right_way):
	"""
	num is 4, 5, 6, 8, 9, or 10, i.e. possible points on which a pass, don't pass, come or don't come bet Odds are placed
	bet is what person wants to win behind the pass, don't pass, come or don't come line
	right_way is boolean indicating if betting Pass/Come (True) or Don't Pass/Come (False) side of point
	"""
	if right_way:
		return bet
	else:
		if num == 4 or num == 10:
			return int(bet * 2)  # e.g. place $20 to win $10
		elif num == 5 or num == 9:
			return int(bet * 3 / 2)  # e.g. place $15 to win $10
		elif num == 6 or num == 8:
			return int(bet * 6 / 5)   # e.g. place $12 to win $10
