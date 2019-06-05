import random, pylab, numpy

#set line width
pylab.rcParams['lines.linewidth'] = 1
#set font size for titles 
pylab.rcParams['axes.titlesize'] = 16
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 16
#set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
#set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
#set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
#set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
#set size of markers
pylab.rcParams['lines.markersize'] = 10
#set number of examples shown in legends
pylab.rcParams['legend.numpoints'] = 1

def plot_sessions (y_values_list, x_values_list, max_y, min_y, max_x):
	"""
	y_values_list = list of lists containing shooter ending pot amounts, e.g. [310, 350, 335, 320, 280...] for each session
	x_values_list = list of lists containing count of shooter rolls, e.g. [1, 2, 3, 4, 5...] for each session
	max_y = the maximum pot amount at which any session ended
	min_y = the mimimum pot amount at which any session ended
	max_x = the maximum number of shooter rolls for all sessions
	"""
	pylab.title('Session Ending Pots vs. # Shooters')
	pylab.xlabel('Number of Shooters')
	pylab.ylabel('Ending Pot Amount')
	pylab.ylim([min_y, max_y])
	pylab.xlim([0, max_x])

	for x in range(len(y_values_list)):
		yVals = pylab.array(y_values_list[x])
		xVals = pylab.array(x_values_list[x])
		pylab.plot(xVals, yVals, 'black')

	pylab.show()