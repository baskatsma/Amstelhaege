import matplotlib.patches as patches
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

        # Increase recursion maximum to obtain 60 house results easier
        sys.setrecursionlimit(4000)

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
        numpyGrid = np.zeros((gridYLength,gridXLength), dtype='object')
        # numpyGrid = np.zeros((gridYLength,gridXLength))

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
                drawNumber = 3

                # Free area and water do not interfere
                visualizeOnGrid(currentObject.yBegin, currentObject.yEnd,
                                currentObject.xBegin, currentObject.xEnd,
                                numpyGrid, drawNumber)

            # Put houses on grid and calculate score
            else:

                # Update uniqueID and place houses
                currentObject.uniqueID = object + 10
                placeOnGrid(currentObject, numpyGrid)

        # After placing all houses, loop over them
        for object in range(len(residentialArea)):

            # Give the current object an easy variable
            currentObject = residentialArea[object]

            # Calculate score if current item is not water
            if currentObject.type != "water":

                # Find all extra free area per house
                increase = (1 * 2)
                numpyGridOriginal = numpyGrid
                checkAllFreeArea(currentObject, increase, numpyGrid,
                                 numpyGridOriginal)

                # Then, calculate the new value of the house
                totalScore += currentObject.calculateScore()

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

        # Visualize grid with matplotlib
        printPlot(residentialArea, totalScore)

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

    # ALLES moet hier 0 zijn in dit gebied om een huis te plaatsen,
    # dus IETS wat ook maar geen 0 is (aka niet leeg), wordt gelijk gecanceld.
    if choice == "excludingFreeArea":

        # Check house dimension area if it's completely empty
        if np.any(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] != 0):
            return False

        else:
            return True

    # We willen kijken of dit gebied OF helemaal 0 (leeg) is, OF helemaal 1
    # (inclusief vrijstand dus, want die mag overlappen)
    # OF een mix van 0 en 1 (leeg + vrijstand)
    # In ieder geval geen 3, 4, 5, etc. of uniqueID waarde.
    if choice == "includingFreeArea":
        if np.all(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] <= 1):
            return True

        else:
            return False

def checkAllFreeArea(currentObject, increase, numpyGrid, numpyGridOriginal):

    # Remove all modifications before (re)starting
    numpyGrid = numpyGridOriginal

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

        # Update extra free area in self
        currentObject.extraFreeArea = increase

        # testing
        print(currentObject.type,"ID:",currentObject.uniqueID,"(",\
        currentObject.yBegin,",",currentObject.xBegin,")","|| increase:",increase)

        # Increase X, Y and call self until impossible
        increase += 2
        checkAllFreeArea(currentObject, increase, numpyGrid, numpyGridOriginal)

    else:

        # Re-draw number, because we deleted it a few steps ago
        numpyGrid[yBegin:yEnd,xBegin:xEnd] = drawNumber

        # Remove all other modifications before ending
        numpyGrid = numpyGridOriginal

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

        # Start over, because there are house and/or free area overlap issues
        else:
            placeOnGrid(currentObject, numpyGrid)

    # Start over, because the house is overlining the border
    else:
        placeOnGrid(currentObject, numpyGrid)

def visualizeOnGrid(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, drawNumber):

    # Select a specific grid area and fill it
    numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] = drawNumber

def printPlot(residentialArea, totalScore):

    # Initialize matplotlib and figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Add title
    plt.title(str(totalScore) + " euro, bitch!")

    # Loop over all objects
    for object in residentialArea:

        # Initialize variables
        yBegin = object.yBegin
        yEnd = object.yEnd
        xBegin = object.xBegin
        xEnd = object.xEnd
        fA = object.freeArea

        # Define color for free area
        colorChoice = 'gray'

        # Define color for house
        if object.type == "eengezinswoning":
            colorChoice2 = 'red'

        elif object.type == "bungalow":
            colorChoice2 = 'green'

        elif object.type == "maison":
            colorChoice2 = 'yellow'

        elif object.type == "water":
            colorChoice2 = 'blue'

        # Create new rects for freeArea + house
        rectUpperRight = patches.Rectangle((xBegin,yBegin),         # (X,Y) tuple
                                 xEnd - xBegin + fA,                # width
                                 yEnd - yBegin + fA,                # height
                                 color=colorChoice,
                                 alpha=0.2)

        rectUpperLeft = patches.Rectangle((xBegin - fA,yBegin),     # (X,Y) tuple
                                 xEnd - xBegin + fA,                # width
                                 yEnd - yBegin + fA,                # height
                                 color=colorChoice,
                                 alpha=0.2)

        rectLowerRight = patches.Rectangle((xEnd + fA,yEnd),        # (X,Y) tuple
                                 xBegin - xEnd - fA,                # width
                                 yBegin - yEnd - fA,                # height
                                 color=colorChoice,
                                 alpha=0.2)

        rectLowerLeft = patches.Rectangle((xEnd,yEnd),              # (X,Y) tuple
                                 xBegin - xEnd - fA,                # width
                                 yBegin - yEnd - fA,                # height
                                 color=colorChoice,
                                 alpha=0.2)

        # Create new rect for house only
        rectHouse = patches.Rectangle((xBegin,yBegin),              # (X,Y) tuple
                                 (xEnd - xBegin),                   # width
                                 (yEnd - yBegin),                   # height
                                 color=colorChoice2,)

        # Add the rects
        ax.add_patch(rectUpperRight)
        ax.add_patch(rectUpperLeft)
        ax.add_patch(rectLowerRight)
        ax.add_patch(rectLowerLeft)
        ax.add_patch(rectHouse)

    # Set figure dimensions
    plt.xlim([0, gridXLength])
    plt.ylim([0, gridYLength])

    # Show matplotlib
    plt.show()
    
    # # Initialize matplotlib
    # plt.figure()
    #
    # # Define grid
    # xGridList = [0, gridXLength, gridXLength, 0, 0]
    # yGridList = [0, 0, gridYLength, gridYLength, 0]
    # plt.plot(xGridList, yGridList)
    #
    # plt.title(str(totalScore) + " euro, bitch!")
    #
    # # Loop over all objects
    # for object in residentialArea:
    #
    #     xCoordinates = [object.xBegin, object.xEnd,
    #     object.xEnd, object.xBegin, object.xBegin]
    #
    #     yCoordinates = [object.yBegin, object.yBegin,
    #     object.yEnd, object.yEnd, object.yBegin]
    #
    #     if object.type == "eengezinswoning":
    #         ePlot = plt.plot(xCoordinates, yCoordinates)
    #         ePlot[0].set_color('r')
    #
    #     elif object.type == "bungalow":
    #         bPlot = plt.plot(xCoordinates, yCoordinates)
    #         bPlot[0].set_color('g')
    #
    #     elif object.type == "maison":
    #         mPlot = plt.plot(xCoordinates, yCoordinates)
    #         mPlot[0].set_color('y')
    #
    #     elif object.type == "water":
    #         mPlot = plt.plot(xCoordinates, yCoordinates)
    #         mPlot[0].set_color('b')
    #
    # # Show matplotlib
    # plt.show()
