# %% Hydrogen run
import numpy as np
import random as rd
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

    # # testing
    maxHouses = 8

    return maxHouses



    # Use uniqueID number to visualize
    drawNumber = currentObject.uniqueID

def getCoordinates(currentObject):

    # Set new begin coordinates (y, x tuple) and save them in self
    currentObject.yBegin = rd.randrange(currentObject.gridYLength)
    currentObject.xBegin = rd.randrange(currentObject.gridXLength)
    beginCoordinates = (currentObject.yBegin, currentObject.xBegin)

    # Extract house dimension values
    houseYLength = currentObject.houseDimensions[1]
    houseXLength = currentObject.houseDimensions[0]

    # Define end coordinates (y, x tuple)
    endCoordinates = (beginCoordinates[0] + houseYLength,
                      beginCoordinates[1] + houseXLength)

    # Update coordinates
    currentObject.yBegin = beginCoordinates[0]
    currentObject.yEnd = endCoordinates[0]
    currentObject.xBegin = beginCoordinates[1]
    currentObject.xEnd = endCoordinates[1]

def checkOverlap(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, choice):

    # newYBegin = currentObject.yBegin
    # newYEnd = currentObject.yEnd
    # newXBegin = currentObject.xBegin
    # newXEnd = currentObject.xEnd

    if choice == "excludingFreeArea":

        # Check house dimension area starting at the begin coordinates
        if np.any(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] != 0):
            print("There's more than 0's")
            return False

        else:
            print("There's room!")
            return True

    if choice == "includingFreeArea":

    # We willen kijken of dit gebied OF helemaal 0 (leeg) is, OF helemaal 1
    # (vrijstand, want die mag overlappen), OF helemaal 2 (water),
    # OF een mix van 0, 1 en 2 (leeg + vrijstand + water)
    # In ieder geval geen 3, 4, 5, etc. of uniqueID waarde.
        if np.all(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] <= 2):
            print("There's room!")
            return True

        else:
            print("There's more than 0 or 1 or 2")
            return False
