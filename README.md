Craps Simulator
===============

Python (developed in V 3.5.0) program that simulates a unique craps strategy whereby minimum table bet amounts are placed on both the Pass & Don't Pass lines to start. Then after a point is established, Come & Don't Come bets are placed to establish more points.  Configurable settings are available for the number of consecutive clean rolls before Odds are placed and the maximum number of Come Bet points that can be made.  Single testing session; multiple sessions with 'walk-away' upper & lower $$$ limits; and multiple session with % ROI results simulation modes are available.

## Help and docs
- [Craps Simulator Code Flow](docs/craps_simulator_shooter_rolls_flow.pdf) - illustration of code flow (with line #s) of CrapsGame class shooter_rolls method.
- [Craps Simulator Outputs](docs/craps_simulator.outputs.pdf) - examples of matplotlib and statistical output.

## To Run Simulator
1) Install [Python (V3.5.0+)](https://www.python.org/)
2) Copy contents of this Repo into a directory
3) Within newly created directory, from command line type:
```bash
python craps_sim.py
```

## Configuration
<b>craps_sim.py</b> - main program that should be run from command line. This is where 3 different simulation 'modes', i.e. functions, are available (comment out at bottom of code as necessary):  
&ensp;(1) <i>crapsTestSim(numRolls)</i> - play x number of rolls with option to print testing information.  Used for testing  
&ensp;(2) <i>crapsSessionSim(numSessions)</i> - play x number of sessions whereby each session concludes when either a user configurable 'walk_away_pot_low' or 'walk_away_pot_high' is reached.  This is a more realistic simulation of craps since people tend to stop when they win or lose a certain amount  
&ensp;(3) <i>crapsROISim(numShooters)</i> - play x number of shooters whereby each shooter rolls until crapping out (i.e. roll 7 after a point is established). A ROI is determined for each shooter which divides the amount won/lost by the $$$ with which the roller started.  
&ensp;&ensp;* Modes #2 & #3 generates statistical data that can be printed after the simulation  
&ensp;&ensp;** Variables within each function determine how simulations are run and craps strategy is employed  

## Other Files
<b>craps.py</b> - module where the main class, 'CrapsGame', resides.  The key method, 'shooter_rolls' contains all the logic and configurable settings for the craps strategy. Other functions are included to produce statistics.

<b>craps_bets.py</b> - module where all methods for making, placing, and laying/removing odds bets located. Player $$ on table and in rail are tracked within each method.  Currently, the following bets are supported: Bet Pass Line, Bet Don't Pass Line, Place Pass Line Odds, Place Don't Pass Line Odds, Pay Pass Line, Pay Don't Pass Line; Bet Come Line, Bet Don't Come Line, Place Come Bet, Place Don't Come Bet, Place/Remove Come Bet Odds, Place/Remove Don't Come Bet Odds, Pay Come Bet, Pay Don't Come Bet

<b>craps_methods.py</b> - module where functions for die rolling, Odds placing and Odds paying located, e.g. rollDie, payOdds, placeOdds

<b>linebet.py</b> - module where the 'LineBet' class is contained with functions for interacting with each Pass & Pass Line bet and Come & Don't Come bet based on established Point

<b>print_methods.py</b> - module where status printing methods to support the craps_roll function are located. 

<b>craps_plot.py</b> - includes new function, plot_sessions, which is called from within craps_sum.py -> crapsSessionSim(numSessions) function.  New variable within crapsSessionSim(numSessions) function called 'plot_results' which controls whether results are plotted prior to publishing statistics.

## Contact Info
For questions or help using and/or setting up this project, contact:  
Paul Maurer  
paulrmaurer1@gmail.com