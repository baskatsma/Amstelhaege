from algorithms import *
from functions import *
from models.templates import *
import os
import sys

def main():

    # Avoid recursion errors
    sys.setrecursionlimit(5000)

    # Initialize variables
    rounds = 1000

    # Initialize algorithms results sheets
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

        return randomResults

    elif str(sys.argv[2]) == "hillclimber":

        # Run random 'rounds' amount of times and use best result
        randomAlgorithm(randomResults)

        # Run hillclimber 'rounds' amount of times and display best results
        hillclimberAlgorithm(hillclimberResults, randomResults)

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

    # Open scores.csv
    with open('scores.csv', 'a', newline='') as csvfile:
        fieldnames = [
            'algorithm',
            'maxHouses',
            'rounds',
            'highestScore',
            'lowestScore',
            'swaps',
            'averageRuntime'
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Only write headers if file is empty
        if os.stat("scores.csv").st_size == 0:
            writer.writeheader()

        # Write the rest
        writer.writerow({
            'algorithm': results.algorithm,
            'maxHouses': results.maxHouses,
            'rounds': results.rounds,
            'highestScore': results.highestScore,
            'lowestScore': results.lowestScore,
            'swaps': results.swaps,
            'averageRuntime': results.averageRuntime
            })
