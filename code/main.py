from hillclimber import *
from functions import *
import sys

def main():

    # Increase recursion maximum to obtain 60 house results easier
    sys.setrecursionlimit(4000)

    # Initialize variables
    rounds = 3500
    roundsCounter = 0

    # Set result template
    allResults = {
                    "allScores": 0,
                    "highestScore": 0,
                    "highestScoreMap": [],
                    "lowestScore": 1000000000,
                    "averageScore": 0,
                    "allRuntimes": 0,
                    "fastestRuntime": 1000000000,
                    "slowestRuntime": 0,
                    "averageRuntime": 0,
                    "totalRuntime": 0,
                    "rounds": rounds,
                    "roundsCounter": roundsCounter,
                    }

    if len(sys.argv) < 3:
        print("You must provide the number of houses and the algorithm!")

    elif str(sys.argv[2]) == "random":

        # Run random 'rounds' amount of times and display best results
        randomAlgorithm(allResults)

    elif str(sys.argv[2]) == "hillclimber":

        #randomMap = initializeRandomMap()
        #hillclimberAlgorithm(randomMap, allResults)
        hillclimberAlgorithm(allResults)

    else:
        print("Not a valid algorithm!")

if __name__ == "__main__":
    main()
