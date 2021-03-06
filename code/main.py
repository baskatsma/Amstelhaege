# Authors:
# Amy van der Gun (10791760)
# Bas Katsma (10787690)
# Felicia van Gastel (11096187)
#
# Amstelhaege
# Programmeertheorie
#
# main.py
# Main file that calls the algorithms and gives the output for a chosen number
# of houses

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

    # Ask user to visualize the algorithm
    print("")
    print("Would you like to visualize the algorithm? It can take a while.")
    print("Enter [1] for YES, or [2] for NO")
    FFmpegChoice = input("")
    if FFmpegChoice != "1" and FFmpegChoice != "2":
        print("Valid input ([1] or [2]), please.")
        print("")
        exit(0)

    # Avoid recursion errors
    sys.setrecursionlimit(5000)

    # Initialize amount of rounds
    rounds = 1000

    # Initialize algorithms results sheets
    templates = []
    randomTemplate = Results(**resultsTemplate)
    hillSwapsTemplate = Results(**resultsTemplate)
    hillMovesTemplate = Results(**resultsTemplate)
    simAnnealingTemplate = Results(**resultsTemplate)
    templates.extend([randomTemplate, hillSwapsTemplate, hillMovesTemplate,
    simAnnealingTemplate])

    # Update rounds & visualization preference
    for template in templates:
        template.rounds = int(rounds)
        template.FFmpegChoice = FFmpegChoice

    # Check whether user inputs the correct amount of arguments
    if len(sys.argv) < 3:
        print("You must provide the number of houses and the algorithm!")

    elif str(sys.argv[2]) == "random":

        # Run random "rounds" amount of times and display best results
        randomResults = randomAlgorithm(randomTemplate)

        return randomResults

    elif str(sys.argv[2]) == "hillSwaps":

        # Run random "rounds" amount of times and use best result
        randomResults = randomAlgorithm(randomTemplate)

        # Run hillclimber "rounds" amount of times and display best results
        hillSwapsResults = hillSwapsAlgorithm(hillSwapsTemplate, \
        randomResults)

        # # Start with a random map
        # randomResult = initializeRandomMap()
        #
        # # Run hillclimber "rounds" amount of times and display best results
        # hillSwapsResults = hillSwapsAlgorithm(hillSwapsTemplate, \
        # randomResult)

        return hillSwapsResults

    elif str(sys.argv[2]) == "hillMoves":

        # Run hillMoves "rounds" amount of times and display best results
        hillMovesResults = hillMovesAlgorithm(hillMovesTemplate,
        "hillMoves")

        return hillMovesResults

    elif str(sys.argv[2]) == "simAnnealing":

        # Run simAnnealing "rounds" amount of times and display best results
        simAnnealingResults = hillMovesAlgorithm(simAnnealingTemplate,
        "simAnnealing")

        return simAnnealingResults

    else:
        print("Not a valid algorithm! Choose among: random, hillSwaps,"
        " hillMoves or simAnnealing")

if __name__ == "__main__":

    results = main()

    if results != None:

        # Visualize algorithm
        if results.FFmpegChoice == "1" and results.algorithm != "random":
            FFmpeg()

        # Visualize map with matplotlib
        residentialArea = results.highestScoreMap
        choice = "printPlot"
        matplotlibCore(residentialArea, choice, 0, results)

        # Write results in scores.csv
        writeResults(results)
