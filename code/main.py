from algorithms import *
from functions import *
from models.templates import *
import sys

def main():

    # Avoid recursion errors
    sys.setrecursionlimit(5000)

    # Initialize variables
    rounds = 1750
    roundsCounter = 0

    if len(sys.argv) < 3:
        print("You must provide the number of houses and the algorithm!")

    elif str(sys.argv[2]) == "random":

        # Initialize random algorithm results sheet
        randomResults = Results(**resultsTemplate)
        randomResults.rounds = rounds

        # Run random 'rounds' amount of times and display best results
        randomAlgorithm(randomResults)

        #getVideo(randomResults.highestScoreMap)
        printPlot(randomResults)

    elif str(sys.argv[2]) == "hillclimber":

        # Initialize both algorithms results sheets
        randomResults = Results(**resultsTemplate)
        randomResults.rounds = rounds

        hillclimberResults = Results(**resultsTemplate)
        hillclimberResults.rounds = rounds * 2

        # Run random 'rounds' amount of times and use best result
        randomAlgorithm(randomResults)

        # Run hillclimber 'rounds' amount of times and display best results
        hillclimberAlgorithm(hillclimberResults, randomResults)

    else:
        print("Not a valid algorithm!")

if __name__ == "__main__":
    main()
