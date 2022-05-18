# This class is only being used by the main class.
# It serves score holding and score functionality.

teamA = 0
teamB = 0

#reset the scores to zero
def resetScore():
    global teamA
    global teamB

    teamA = 0
    teamB = 0

#increments the score for a team | parameter "a" or "b"
def incScore(team):
    global teamA
    global teamB

    if(team.lower() == "a"):
        teamA +=1
    else:
        teamB +=1

#returns the score of a team | parameter "a" or "b"
def getScore(team):
    global teamA
    global teamB

    if(team.lower() == "a"):
        return teamA
    else:
        return teamB