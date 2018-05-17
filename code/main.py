from algorithms import *
from functions import *
from models.templates import *
import sys

def main():

    # Initialize variables
    rounds = 200
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
                    "maxHouses": 0,
                    }

    if len(sys.argv) < 3:
        print("You must provide the number of houses and the algorithm!")

    elif str(sys.argv[2]) == "random":

        print(allResults)

        # Run random 'rounds' amount of times and display best results
        randomAlgorithm(allResults)

        #getVideo(allResults["highestScoreMap"])
        printPlot(allResults)

    elif str(sys.argv[2]) == "hillclimber":

        hillClimberResults["rounds"] = rounds
        hillClimberResults["roundsCounter"] = roundsCounter

        hillclimberAlgorithm(hillClimberResults)

    else:
        print("Not a valid algorithm!")

if __name__ == "__main__":
    main()
