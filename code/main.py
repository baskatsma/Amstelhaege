from algorithms import *
from functions import *
from models.templates import *
import sys

def main():

    # Avoid recursion errors
    sys.setrecursionlimit(5000)

    # Initialize variables
    rounds = 1000

    # Initialize both algorithms results sheets
    randomResults = Results(**resultsTemplate)
    randomResults.rounds = int(rounds)

    hillyTemplate = Results(**resultsTemplate)
    hillyTemplate.rounds = int(rounds * 1.5)

    hillclimberResults = Results(**resultsTemplate)
    hillclimberResults.rounds = int(rounds * 1.5)

    if len(sys.argv) < 3:
        print("You must provide the number of houses and the algorithm!")

    elif str(sys.argv[2]) == "random":

        # Run random 'rounds' amount of times and display best results
        randomAlgorithm(randomResults)

        #getVideo(randomResults.highestScoreMap)
        printPlot(randomResults)

    elif str(sys.argv[2]) == "hillclimber":

        # Run random 'rounds' amount of times and use best result
        randomAlgorithm(randomResults)

        # Run hillclimber 'rounds' amount of times and display best results
        hillclimberAlgorithm(hillclimberResults, randomResults)

    elif str(sys.argv[2]) == "hilly":

        hillyAlgorithm(hillyTemplate)
        printPlot(hillyTemplate)

        # Run hillclimber 'rounds' amount of times and display best results
        #hillclimberAlgorithm(hillclimberResults, hillyResult, "hilly")

    else:
        print("Not a valid algorithm!")

if __name__ == "__main__":
    main()
