# %% Import classes
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from models.models import *
from models.templates import *
from functions import *

# Starting point
def main():

    # Get maxHouses
    maxHouses = defineMaxHouses()

    # Create grid instance
    gridField = Grid(gridXLength, gridYLength, maxHouses)

    # Create numpy grid (verticalY, horizontalX)
    buildingSite = np.zeros((gridYLength,gridXLength),dtype=object)

    # Create woonwijk
    residentialArea = []

    # Create new houses based on the grid requirements
    for eengezinswoning in range(gridField.totalAmountEengezinswoningen):
        residentialArea.append(House(**eengezinswoningTemplate))

    for bungalow in range(gridField.totalAmountBungalows):
        residentialArea.append(House(**bungalowTemplate))
        
    for maison in range(gridField.totalAmountMaisons):
        residentialArea.append(House(**maisonTemplate))

    # Loop over all houses
    for house in range(len(residentialArea)):

        # Update uniqueIDs
        residentialArea[house].uniqueID = house

        # Place houses on grid
        currentHouse = residentialArea[house]
        currentHouse.drawOnGrid(buildingSite, currentHouse)

    # Print buildingSite with some fancy thaaangs
    rowCounter = 0
    print("")
    print("")
    print("        X →")
    print("        ",end="")
    for i in range(gridXLength):
        if i < 10:
            print(i," ",end="")
        else:
            print(i,"",end="")
    print("")
    print("  ↓ Y")
    for row in buildingSite:
        if rowCounter < 10:
            print("   ",rowCounter," ", end="")
        else:
            print("  ",rowCounter," ", end="")

        print(row)
        rowCounter += 1
    print("")
    print("")

    plt.figure()

    # These coordinates together plot the outline of the neighbourhood
    xCoordinateList = [0, gridXLength, gridXLength, 0, 0]
    yCoordinateList = [0, 0, gridYLength, gridYLength, 0]
    plt.plot(xCoordinateList, yCoordinateList)

    for house in residentialArea:

        houseYLength = house.houseDimensions[1]
        houseXLength = house.houseDimensions[0]

        beginCoordinates = (house.yBegin, house.xBegin)

        # Define end coordinates (y, x tuple)
        endCoordinates = (beginCoordinates[0] + houseYLength,
                          beginCoordinates[1] + houseXLength)

        # Define new coordinates
        yCoordinateBegin = beginCoordinates[0]
        yCoordinateEnd = endCoordinates[0]
        xCoordinateBegin = beginCoordinates[1]
        xCoordinateEnd = endCoordinates[1]

        # By plotting these lists, all corners will be connected by a line
        xCoordinateList = [xCoordinateBegin, xCoordinateEnd,
        xCoordinateEnd, xCoordinateBegin, xCoordinateBegin]

        yCoordinateList = [yCoordinateBegin, yCoordinateBegin,
        yCoordinateEnd, yCoordinateEnd, yCoordinateBegin]

        plt.plot(xCoordinateList, yCoordinateList)

    plt.show()

    # # Print test woonwijk
    # for i in range(len(residentialArea)):
    #     print(residentialArea[i].type, "|| uniqueID is:",
    #     residentialArea[i].uniqueID)

    # # Print test extra House functions
    # b = House(**eengezinswoningTemplate)
    # print("")
    # print("B is een " + b.type + " met afmetingen:", b.houseDimensions)
    # print("De waarde van B is: " + str(b.value) + " euro")
    # print("B nieuwe waarde met extra vrijstand (", b.extraFreeArea, "meter )
    # is:", b.calculateNewValue())

# %%
if __name__ == "__main__":
    main()
