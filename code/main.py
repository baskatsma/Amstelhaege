from algorithms import *
from functions import *
from models.templates import *
import os
import sys

def main():
    """
    This function calls the chosen algorithm to create a residential area
    containing 20, 40 or 60 houses.
    """

    # Avoid recursion errors
    sys.setrecursionlimit(5000)

    # Initialize amount of rounds
    rounds = 1000

    # Initialize algorithms results sheets
    randomTemplate = Results(**resultsTemplate)
    randomTemplate.rounds = int(rounds)

    hillSwapsTemplate = Results(**resultsTemplate)
    hillSwapsTemplate.rounds = int(rounds)

    hillMovesTemplate = Results(**resultsTemplate)
    hillMovesTemplate.rounds = int(rounds)

    simAnnealingTemplate = Results(**resultsTemplate)
    simAnnealingTemplate.rounds = int(rounds)

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

    elif str(sys.argv[2]) == "hillSwaps":

        # Run random "rounds" amount of times and use best result
        randomResults = randomAlgorithm(randomTemplate)

        # Run hillclimber "rounds" amount of times and display best results
        hillSwapsResults = hillSwapsAlgorithm(hillSwapsTemplate, \
        randomResults)

        # Visualize grid with matplotlib
        printPlot(hillSwapsResults)

        return hillSwapsResults

    elif str(sys.argv[2]) == "hillMoves":

        # Run hillMoves "rounds" amount of times and display best results
        hillMovesResults = hillMovesAlgorithm(hillMovesTemplate, \
        "hillMoves")

        # Visualize grid with matplotlib
        printPlot(hillMovesResults)

        return hillMovesResults

    elif str(sys.argv[2]) == "simAnnealing":

        # Run simAnnealing "rounds" amount of times and display best results
        simAnnealingResults = hillMovesAlgorithm(simAnnealingTemplate, \
        "simAnnealing")

        # Visualize grid with matplotlib
        printPlot(simAnnealingResults)

        return simAnnealingResults

    else:
        print("Not a valid algorithm! Choose among: random, hillSwaps," \
        " hillMoves or simAnnealing")

if __name__ == "__main__":
    results = main()

    if results != None:
        writeResults(results)
