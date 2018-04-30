# %% Hydrogen run
import sys

# %% Define residential area size (either 20, 40 or 60 houses at max)
def defineMaxHouses():

    # 20 by default, unless specified
    maxHouses = 20

    # Check if a number is entered in the CLI
    if len(sys.argv) == 1:
        print("maxHouses remains 20")

    # Check if the number is valid (either 20, 40 or 60)
    elif len(sys.argv) == 2:
        if str(sys.argv[1]) == "20":
            print("sys.argv = 20, maxHouses remains 20")
        elif str(sys.argv[1]) == "40":
            maxHouses = 40
            print("sys.argv = 40, maxHouses = 40")
        elif str(sys.argv[1]) == "60":
            maxHouses = 60
            print("sys.argv = 60, maxHouses = 60")
        # Else default to 20
        else:
            maxHouses = 20
            print("sys.argv is an invalid number, maxHouses = 20 by default")

    # Testing purposes
    maxHouses = 16
    
    return maxHouses
