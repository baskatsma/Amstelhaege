from functions import *

def main():

    if not len(sys.argv) == 3:
        print("You must provide the number of houses and the algorithm!")
    elif str(sys.argv[2]) == "random":
        randomAlgorithm()
    elif str(sys.argv[2]) == "hillclimber":
        hillclimberAlgorithm()
    elif len(sys.argv) < 3:
        randomAlgorithm()

if __name__ == "__main__":
    main()
