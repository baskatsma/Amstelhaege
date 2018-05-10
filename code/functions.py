import matplotlib.pyplot as plt
import numpy as np
import random as rd
import sys
from timeit import default_timer as timer
from models.models import *
from models.templates import *

# Run random algorithm
def randomAlgorithm():

        # Measure algorithm time
        timeStart = timer()

        # Get maxHouses
        maxHouses = defineSettings()

        # Create a grid helper instance
        gridInformation = GridInformation(gridXLength, gridYLength, maxHouses)

        # Create woonwijk
        residentialArea = []

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

            # Put water on grid
            if currentObject.type == "water":

                # Set its coordinates and update uniqueID
                updateCoordinates(currentObject, (0, 0))
                currentObject.uniqueID = object + 200
                #drawNumber = currentObject.uniqueID
                drawNumber = 2

                # Free area and water do not interfere
                visualizeOnGrid(currentObject.yBegin, currentObject.yEnd,
                                currentObject.xBegin, currentObject.xEnd,
                                numpyGrid, drawNumber)

            # Put houses on grid and calculate score
            else:

                # Update uniqueID and place houses
                currentObject.uniqueID = object + 10
                placeOnGrid(currentObject, numpyGrid)

        for object in range(len(residentialArea)):

            currentObject = residentialArea[object]

            # Calculate score
            if currentObject.type != "water":
                increase = 1
                checkAllFreeArea(currentObject, increase, numpyGrid)
                totalScore += currentObject.calculateScore()

                print(currentObject.type, "|| uniqueID is:",
                currentObject.uniqueID," || eFA is:", currentObject.extraFreeArea)

        # Print score
        print("The total score is:", totalScore)

        # # TERMINAL
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

        timeEnd = timer()

        print("Elapsed time (in seconds):",timeEnd - timeStart)
        print("")

        printPlot(residentialArea)

        # # Print test woonwijk
        # for i in range(len(residentialArea)):
        #     print(residentialArea[i].type, "|| uniqueID is:",
        #     residentialArea[i].uniqueID)

# Define residential area size (either 20, 40 or 60 houses at max)
def defineSettings():

    # 20 houses by default, unless specified
    maxHouses = 20

    # Check if arguments are entered in the CLI
    if len(sys.argv) == 1:
        maxHouses = 20

    elif len(sys.argv) >= 2:

        # Check if the number is valid (either 20, 40 or 60)
        if str(sys.argv[1]) == "20":
            maxHouses = 20
        elif str(sys.argv[1]) == "40":
            maxHouses = 40
        elif str(sys.argv[1]) == "60":
            maxHouses = 60

        # Else default to 20 houses
        else:
            maxHouses = 20

    # TERMINAL
    # maxHouses = 8

    return maxHouses

def getCoordinates(currentObject):

    # Set new begin coordinates (y, x tuple) and save them in self
    currentObject.yBegin = rd.randrange(currentObject.gridYLength)
    currentObject.xBegin = rd.randrange(currentObject.gridXLength)
    beginCoordinates = (currentObject.yBegin, currentObject.xBegin)

    # Extract object dimension (x, y tuple) values
    objectYLength = currentObject.objectDimensions[1]
    objectXLength = currentObject.objectDimensions[0]

    # Define end coordinates (y, x tuple)
    endCoordinates = (beginCoordinates[0] + objectYLength,
                      beginCoordinates[1] + objectXLength)

    # Update coordinates
    currentObject.yBegin = beginCoordinates[0]
    currentObject.yEnd = endCoordinates[0]
    currentObject.xBegin = beginCoordinates[1]
    currentObject.xEnd = endCoordinates[1]

def updateCoordinates(currentObject, coordinates):

    # Extract water dimension values
    objectYLength = currentObject.objectDimensions[0]
    objectXLength = currentObject.objectDimensions[1]

    # Define end coordinates (y, x tuple)
    endCoordinates = (coordinates[0] + objectYLength,
                      coordinates[1] + objectXLength)

    # Update coordinates
    currentObject.yBegin = coordinates[0]
    currentObject.yEnd = endCoordinates[0]
    currentObject.xBegin = coordinates[1]
    currentObject.xEnd = endCoordinates[1]

def checkOverlap(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, choice):

    if choice == "excludingFreeArea":

        # Check house dimension area starting at the begin coordinates
        if np.any(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] != 0):
            return False

        else:
            return True

    if choice == "includingFreeArea":

    # We willen kijken of dit gebied OF helemaal 0 (leeg) is, OF helemaal 1
    # (vrijstand, want die mag overlappen)
    # OF een mix van 0 en 1 (leeg + vrijstand)
    # In ieder geval geen 3, 4, 5, etc. of uniqueID waarde.
        if np.all(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] <= 1):
            return True

        else:
            return False

def checkAllFreeArea(currentObject, increase, numpyGrid):

    # Define coordinate variables
    yBegin = currentObject.yBegin
    yEnd = currentObject.yEnd
    xBegin = currentObject.xBegin
    xEnd = currentObject.xEnd
    freeArea = currentObject.freeArea

    fAYBegin = yBegin - freeArea
    fAYEnd = yEnd + freeArea
    fAXBegin = xBegin - freeArea
    fAXEnd = xEnd + freeArea

    # Get drawNumbers
    # TERMINAL
    drawNumber = currentObject.uniqueID
    fADrawNumber = 1

    # Change uniqueID drawnumber to 1's for this method to work
    numpyGrid[yBegin:yEnd,xBegin:xEnd] = fADrawNumber

    # Check if new area contains only empty-values or free area-values
    if np.all(numpyGrid[fAYBegin - increase:fAYEnd + increase,
            fAXBegin - increase:fAXEnd + increase] <= 1) and \
            currentObject.checkBorders() == True:

        # Increase X, Y and call self until impossible
        increase += 1
        checkAllFreeArea(currentObject, increase, numpyGrid)

    else:
        # Update extra free area in self
        currentObject.extraFreeArea = increase

        # Re-draw number, because we deleted it a few steps ago
        numpyGrid[yBegin:yEnd,xBegin:xEnd] = drawNumber

        return False

def placeOnGrid(currentObject, numpyGrid):

    # Get random coordinates and update in self
    getCoordinates(currentObject)

    # # TERMINAL
    # if currentObject.type == "eengezinswoning":
    #     currentObject.freeArea = 1
    #     drawNumber = 3
    #
    # elif currentObject.type == "bungalow":
    #     currentObject.freeArea = 1
    #     drawNumber = 4
    #
    # elif currentObject.type == "maison":
    #     currentObject.freeArea = 2
    #     drawNumber = 5
    #
    # elif currentObject.type == "water":
    #     currentObject.freeArea = 0
    #     drawNumber = 2

    yBegin = currentObject.yBegin
    yEnd = currentObject.yEnd
    xBegin = currentObject.xBegin
    xEnd = currentObject.xEnd
    freeArea = currentObject.freeArea

    fAYBegin = yBegin - freeArea
    fAYEnd = yEnd + freeArea
    fAXBegin = xBegin - freeArea
    fAXEnd = xEnd + freeArea

    # Get drawNumbers
    # TERMINAL
    drawNumber = currentObject.uniqueID
    fADrawNumber = 1

    # Check for grid border problems
    if currentObject.checkBorders() == True:

        # Check for house and free area overlap
        if checkOverlap(yBegin, yEnd, xBegin, xEnd, numpyGrid,
                        "excludingFreeArea") == True and \
        checkOverlap(fAYBegin, fAYEnd, fAXBegin, fAXEnd, numpyGrid,
                    "includingFreeArea") == True:

            # The area is viable: draw free area first
            visualizeOnGrid(fAYBegin, fAYEnd, fAXBegin, fAXEnd,
                            numpyGrid, fADrawNumber)

            # Visualize house on top of free area
            visualizeOnGrid(yBegin, yEnd, xBegin, xEnd, numpyGrid, drawNumber)

        # Start over with drawOnGrid for this specific house
        else:
            placeOnGrid(currentObject, numpyGrid)

    else:
        placeOnGrid(currentObject, numpyGrid)

def visualizeOnGrid(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, drawNumber):

    # Select a specific grid area and fill it
    numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] = drawNumber

def printPlot(residentialArea):

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
