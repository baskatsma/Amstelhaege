from algorithms import *
from functions import *
from models.templates import *
import os
import sys

def main():

    # Avoid recursion errors
    sys.setrecursionlimit(5000)

    # Initialize variables
    rounds = 10

    # Initialize algorithms results sheets
    randomTemplate = Results(**resultsTemplate)
    randomTemplate.rounds = int(rounds)

    hillyTemplate = Results(**resultsTemplate)
    hillyTemplate.rounds = int(rounds * 1.5)

    hillclimberTemplate = Results(**resultsTemplate)
    hillclimberTemplate.rounds = int(rounds * 1.5)

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
        hillclimberResults = hillclimberAlgorithm(hillclimberTemplate, randomResults)

        # Visualize grid with matplotlib
        printPlot(hillclimberResults)

        return hillclimberResults

    elif str(sys.argv[2]) == "hilly":

        hillyAlgorithm(hillyTemplate, "hilly")
        printPlot(hillyTemplate)

        return hillyTemplate

    elif str(sys.argv[2]) == "simmy":

        hillyAlgorithm(hillyTemplate, "simmy")
        printPlot(hillyTemplate)

        return hillyTemplate

    else:
        print("Not a valid algorithm!")

if __name__ == "__main__":
    results = main()

    writeResults(results)
