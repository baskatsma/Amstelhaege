from algorithms import *
from functions import *
from models.templates import *
import sys

def main():

    # Avoid recursion errors
    sys.setrecursionlimit(5000)

    # Initialize variables
    rounds = 500

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

        with open('scores.csv', 'w', newline='') as csvfile:
            fieldnames = ['algorithm', 'highestScore', 'lowestScore', 'averageScore', 'runtime', 'maxHouses']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Run random 'rounds' amount of times and display best results
            randomAlgorithm(randomResults)

            writer.writeheader()
            writer.writerow({'algorithm': 'Random', 'highestScore': randomResults.highestScore, 'lowestScore': randomResults.lowestScore, 'averageScore': randomResults.averageScore, 'runtime': randomResults.averageRuntime, 'maxHouses': randomResults.runtime})

        #getVideo(randomResults.highestScoreMap)
        printPlot(randomResults)

    elif str(sys.argv[2]) == "hillclimber":

        # Run random 'rounds' amount of times and use best result
        randomAlgorithm(randomResults)

        # Run hillclimber 'rounds' amount of times and display best results
        hillclimberAlgorithm(hillclimberResults, randomResults)

    elif str(sys.argv[2]) == "hilly":

        hillyAlgorithm(hillyTemplate, "hilly")
        printPlot(hillyTemplate)

    elif str(sys.argv[2]) == "simmy":

        hillyAlgorithm(hillyTemplate, "simmy")
        printPlot(hillyTemplate)

    else:
        print("Not a valid algorithm!")

if __name__ == "__main__":
    main()
