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
    FFmpegChoice = int(input(""))
    if FFmpegChoice == None:
        exit(0)

    # Avoid recursion errors
    sys.setrecursionlimit(5000)

    # Initialize amount of rounds
    rounds = 400

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

        # Visualize grid with matplotlib
        if FFmpegChoice == 1:
            getVideo(randomResults, "random")

        printPlot(randomResults)

        return randomResults

    elif str(sys.argv[2]) == "hillSwaps":

        # Run random "rounds" amount of times and use best result
        randomResults = randomAlgorithm(randomTemplate)

        # Run hillclimber "rounds" amount of times and display best results
        hillSwapsResults = hillSwapsAlgorithm(hillSwapsTemplate, \
        randomResults)

        # Visualize grid with matplotlib
        if FFmpegChoice == 1:
            FFmpeg()

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
