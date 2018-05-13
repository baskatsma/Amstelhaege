from functions import *
import sys

def main():

    if len(sys.argv) < 3:
        print("You must provide the number of houses and the algorithm!")
    elif str(sys.argv[2]) == "random":
        randomAlgorithm()
    elif str(sys.argv[2]) == "hillclimber":
        hillclimberAlgorithm()
    else:
        print("Not a valid algorithm!")

if __name__ == "__main__":
    main()
