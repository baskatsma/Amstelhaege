# %% Import classes
import numpy as np
import matplotlib.pyplot as plt
from models.models import *
from models.templates import *
from functions import *

def main():

    # Get maxHouses
    maxHouses = defineMaxHouses()

    # Create grid instance
    gridInformation = GridInformation(gridXLength, gridYLength, maxHouses)

    # Create woonwijk
    residentialArea = []
    testwijk = []

    testwijk.append(House(**eengezinswoningTemplate))
    # Loop over all objects (water + houses)
    for object in range(len(testwijk)):

        # Give the current object an easy variable
        currentObject = testwijk[object]

        # Update uniqueID and put water on grid
        getCoordinates(currentObject)
        print(currentObject.yBegin)
        print(currentObject.yEnd)
        print(currentObject.xBegin)
        print(currentObject.xEnd)

    # Add one piece of water
    residentialArea.append(Water(**waterTemplate))

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

    # Loop over all objects (water + houses)
    for object in range(len(residentialArea)):

        # Give the current object an easy variable
        currentObject = residentialArea[object]

        newYBegin = currentObject.yBegin
        newYEnd = currentObject.yEnd
        newXBegin = currentObject.xBegin
        newXEnd = currentObject.xEnd

        # Update uniqueID and put water on grid
        if currentObject.type == "water":
            currentObject.uniqueID = object + 200
            checkOverlap(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, "houses")
            currentObject.drawOnGrid(numpyGrid)

        # Update uniqueIDs, put houses on grid and calculate score
        else:
            currentObject.uniqueID = object + 10
            checkOverlap(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, "houses")
            currentObject.drawOnGrid(numpyGrid)
            totalScore += currentObject.calculateScore()

        # checkOverlap(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, "houses")
        # currentObject.drawOnGrid(numpyGrid)

    # Print score
    print("The total score is:", totalScore)

    # # Print numpyGrid with some fancy thaaangs
    # rowCounter = 0
    # print("")
    # print("")
    # print("        X →")
    # print("        ",end="")
    # for i in range(gridXLength):
    #     if i < 10:
    #         print(i," ",end="")
    #     else:
    #         print(i,"",end="")
    # print("")
    # print("  ↓ Y")
    # for row in numpyGrid:
    #     if rowCounter < 10:
    #         print("   ",rowCounter," ", end="")
    #     else:
    #         print("  ",rowCounter," ", end="")
    #
    #     print(row)
    #     rowCounter += 1
    # print("")
    # print("")

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

        elif object.type == "water":
            mPlot = plt.plot(xCoordinates, yCoordinates)
            mPlot[0].set_color('b')

    # Show matplotlib
    plt.show()

    # Print test woonwijk
    # for i in range(len(residentialArea)):
    #     print(residentialArea[i].type, "|| uniqueID is:",
    #     residentialArea[i].uniqueID)

# %%
if __name__ == "__main__":
    main()
