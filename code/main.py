from algorithms import *
from functions import *
from models.templates import *
import os
import sys

def main():
    """
    Calls the chosen algorithm to create a residential area
    containing 20, 40 or 60 houses.
    """

    # Avoid recursion errors
    sys.setrecursionlimit(5000)

    # Initialize amount of rounds
    rounds = 1000

    # Initialize algorithms results sheets
    randomTemplate = Results(**resultsTemplate)
    randomTemplate.rounds = int(rounds)

    hillclimberTemplate = Results(**resultsTemplate)
    hillclimberTemplate.rounds = int(rounds)

    hillyTemplate = Results(**resultsTemplate)
    hillyTemplate.rounds = int(rounds)

    # Check whether user inputs the correct amount of arguments
    if len(sys.argv) < 3:
        print("You must provide the number of houses and the algorithm!")

    elif str(sys.argv[2]) == "random":

        # Run random "rounds" amount of times and display best results
        randomResults = randomAlgorithm(randomTemplate)

        # Visualize grid with matplotlib
        #getVideo(randomResults.highestScoreMap)
        printPlot(randomResults)

        return randomResults

    elif str(sys.argv[2]) == "hillclimber":

        # Run random "rounds" amount of times and use best result
        randomResults = randomAlgorithm(randomTemplate)

        # Run hillclimber "rounds" amount of times and display best results
        hillclimberResults = hillclimberAlgorithm(hillclimberTemplate, \
        randomResults)

        # Visualize grid with matplotlib
        printPlot(hillclimberResults)

        return hillclimberResults

    elif str(sys.argv[2]) == "hilly":

        # Run hilly "rounds" amount of times and display best results
        hillyResults = hillyAlgorithm(hillyTemplate, "hilly")

        # Visualize grid with matplotlib
        printPlot(hillyResults)

        return hillyResults

    elif str(sys.argv[2]) == "simmy":

        # Run simmy "rounds" amount of times and display best results
        simmyResults = hillyAlgorithm(hillyTemplate, "simmy")

        # Visualize grid with matplotlib
        printPlot(simmyResults)

        return simmyResults

    else:
        print("Not a valid algorithm! Choose among: random, hillclimber, hilly\
        or simmy")

if __name__ == "__main__":
    results = main()

    if results != None:
        writeResults(results)
