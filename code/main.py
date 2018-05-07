# %% Import classes
import numpy as np
import matplotlib.pyplot as plt
from models.models import *
from models.templates import *
from functions import *

# Starting point
def main():

    # Get maxHouses
    maxHouses = defineMaxHouses()

    # Create grid instance
    gridInformation = GridInformation(gridXLength, gridYLength, maxHouses)

    # Create woonwijk
    residentialArea = []

    # Create new houses based on the grid requirements
    for eengezinswoning in range(gridInformation.totalAmountEengezinswoningen):
        residentialArea.append(House(**eengezinswoningTemplate))

    for bungalow in range(gridInformation.totalAmountBungalows):
        residentialArea.append(House(**bungalowTemplate))

    for maison in range(gridInformation.totalAmountMaisons):
        residentialArea.append(House(**maisonTemplate))

    # Initialize numpy grid (verticalY, horizontalX)
    # numpyGrid = np.zeros((gridYLength,gridXLength),dtype=object)
    numpyGrid = np.zeros((gridYLength,gridXLength))

    # Initialize total score
    totalScore = 0

    # Loop over all houses
    for house in range(len(residentialArea)):

        # Give the current house an easy variable
        currentHouse = residentialArea[house]

        # Update uniqueIDs (starting at 10)
        currentHouse.uniqueID = house + 10

        # Place houses on grid and calculate total score
        currentHouse.drawOnGrid(numpyGrid)
        totalScore += currentHouse.calculateScore()

    print("The total score is:", totalScore)

    # Print numpyGrid with some fancy thaaangs
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
    for row in numpyGrid:
        if rowCounter < 10:
            print("   ",rowCounter," ", end="")
        else:
            print("  ",rowCounter," ", end="")

        print(row)
        rowCounter += 1
    print("")
    print("")

    # Initialize matplotlib
    plt.figure()

    # Define grid
    xGridList = [0, gridXLength, gridXLength, 0, 0]
    yGridList = [0, 0, gridYLength, gridYLength, 0]
    plt.plot(xGridList, yGridList)

    # Loop over all objects
    for object in residentialArea:

        xCoordinates = [object.xBegin, object.xEnd,
        object.xEnd, object.xBegin, object.xBegin]

        yCoordinates = [object.yBegin, object.yBegin,
        object.yEnd, object.yEnd, object.yBegin]

        if object.type == "eengezinswoning":
            ePlot = plt.plot(xCoordinates, yCoordinates)
            ePlot[0].set_color('r')

        elif object.type == "bungalow":
            bPlot = plt.plot(xCoordinates, yCoordinates)
            bPlot[0].set_color('g')

        elif object.type == "maison":
            mPlot = plt.plot(xCoordinates, yCoordinates)
            mPlot[0].set_color('y')

    # Show matplotlib
    plt.show()

    # # Print test woonwijk
    # for i in range(len(residentialArea)):
    #     print(residentialArea[i].type, "|| uniqueID is:",
    #     residentialArea[i].uniqueID)

# %%
if __name__ == "__main__":
    main()
