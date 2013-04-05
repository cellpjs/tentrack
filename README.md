## tentrack ##
is a simple web application for keeping track of tennis match results

Each player is assigned a point which is updated weekly based on the results of matches played in the previous week

Players are ranked by point

### Scoreboard ###
shows the current points and ranks of players based on match results up to last week

clicking on a player name takes you to player view

### Player View ###
shows all the match results of the player

### OPEN week ###
shows the match results of the week in progress and has the link for posting new match results

### Post ###
Lets you choose the two players of the winning team, the score, and the two players of the losing team

Pressing the Post button uploads the data

The form prevents posting incomplete or duplicate results 

### Weekly match results ###
shows the match results for each week

### Play Matrix ###
displays a 2 dimensional heat map of which players played with which players  
 
### Computation of Points ###
Each player starts with 800 points at the beginning of the league. Calculation of points for each match is based on the [Elo rating system](http://en.wikipedia.org/wiki/Elo_rating_system) used in Chess leagues. The points earned by winner is inversely proportional to the odds of the winning (lower the odds, higher the points) where the odds are based on previous points. The losing team loses half of the points earned by the winning team.

	R_w = average point of winning team (up to last week)  
	R_l = average point of losing team (up to last week)  
	Q_w = math.pow(10,R_w/400.) "power" of the winning team  
	Q_l = math.pow(10,R_l/400.) "power" of the losing team  
	E_w = Q_w/(Q_w+Q_l) "probability" that the winning team will win (e.g., 0.5 if average points are equal)  
	Points earned by winnig team members = 32*(1-E_w)
 

Example:

	A(1000pt)/B(990pt) def. C(1100pt)/D(980pt)  
	R_w = 995, R_l = 1040  
	Q_w = 307., Q_l = 398.  
	E_w = 0.4356  
	winning team earns 18 points, losing team losses 9 points

### Closing a week ###

Points are applied at the end of the week by running  
`python manage.py closeweek`

This can be scheduled by crontab to run at a certain time every week

### Admin interface ###

Add player

Delete match posted with error







