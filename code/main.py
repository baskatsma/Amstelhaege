from functions import *
import sys

def main():

    # Increase recursion maximum to obtain 60 house results easier
    sys.setrecursionlimit(4000)

    if len(sys.argv) < 3:
        print("You must provide the number of houses and the algorithm!")

    elif str(sys.argv[2]) == "random":

        # Initialize variables
        rounds = 2000
        roundsCounter = 0
        bestResults = []
        bestResults.append(0)

        # Run random 'rounds' amount of times and display best results
        randomAlgorithm(rounds, roundsCounter, bestResults)

    elif str(sys.argv[2]) == "hillclimber":
        hillclimberAlgorithm()

    else:
        print("Not a valid algorithm!")

if __name__ == "__main__":
    main()
