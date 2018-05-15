import glob
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import os
import random as rd
import sys
from models.models import *
from models.templates import *
from timeit import default_timer as timer

# Run random algorithm
def randomAlgorithm(allResults):

        # Update round
        allResults["roundsCounter"] += 1

        # Remove old output results
        for png in glob.glob("tmp/*.png"):
            os.remove(png)

        for mp4 in glob.glob("tmp/*.mp4"):
            os.remove(mp4)

        # Measure algorithm time
        timeStart = timer()

        # Get a random map
        randomMap = initializeRandomMap()

        # Extract map and results
        residentialArea = randomMap[0]
        numpyGrid = randomMap[1]
        currentResult = randomMap[2]

        # Print score
        print("The total score is:", currentResult["score"])

        # Update algorithm runtime
        timeEnd = timer()
        runtime = (timeEnd - timeStart)

        # Save current results
        currentResult["runtime"] = runtime
        currentResult["residentialArea"] = residentialArea

        # Update allResults template with the current results
        allResults["maxHouses"] = currentResult["maxHouses"]
        allResults["totalRuntime"] += runtime

        # Based on the current results, check for higher/lower scores and update
        allResults = updateResults(currentResult, allResults)

        # Print runtime
        print("Total elapsed time (in seconds):",allResults["totalRuntime"])
        print("")

        # Only run 'rounds' amount of times
        if allResults["roundsCounter"] < allResults["rounds"]:
            randomAlgorithm(allResults)

        else:
            # Print high/low score & runtime
            print("")
            print("Rounds:", allResults["rounds"], "|| MaxHouses:", \
            allResults["maxHouses"])
            print("---------------------------------------------")
            print("Highest score:", allResults["highestScore"])
            print("Lowest score:", allResults["lowestScore"])
            print("Average score:", allResults["averageScore"])
            print("---------------------------------------------")
            print("Fastest runtime (sec):", allResults["fastestRuntime"])
            print("Slowest runtime (sec):", allResults["slowestRuntime"])
            print("Average runtime (sec):", allResults["averageRuntime"])
            print("---------------------------------------------")
            print("Total runtime (sec):", allResults["totalRuntime"])
            print("")
            #getVideo(allResults["highestScoreMap"])
            printPlot(allResults)

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

def initializeRandomMap():

    # Get maxHouses
    maxHouses = defineSettings()

    # Create a grid helper instance
    gridInformation = GridInformation(gridXLength, gridYLength, maxHouses)

    # Create woonwijk
    residentialArea = []

    # Add one piece of water
    residentialArea.append(Water(**waterTemplate))

    # Create new houses based on the grid requirements
    for maison in range(gridInformation.totalAmountMaisons):
        residentialArea.append(House(**maisonTemplate))

    for bungalow in range(gridInformation.totalAmountBungalows):
        residentialArea.append(House(**bungalowTemplate))

    for eengezinswoning in range(gridInformation.totalAmountEengezinswoningen):
        residentialArea.append(House(**eengezinswoningTemplate))

    # Initialize numpy grid (verticalY, horizontalX)
    numpyGrid = np.zeros((gridYLength,gridXLength), dtype='object')

    # Initialize current score
    currentResult = {
                    "score": 0,
                    "runtime": 0,
                    "residentialArea": [],
                    "maxHouses": maxHouses,
                    }

    # Loop over all objects (water + houses)
    for object in range(len(residentialArea)):

        # Give the current object an easy variable
        currentObject = residentialArea[object]

        # Put water on numpy grid
        if currentObject.type == "water":

            # Set its coordinates and update uniqueID
            updateCoordinates(currentObject, (0, 0))
            currentObject.uniqueID = 200

            # Define the number in the numpy grid
            drawNumber = 3

            # Immediately plot it, as the field is empty at the moment
            visualizeOnGrid(currentObject.yBegin, currentObject.yEnd,
                            currentObject.xBegin, currentObject.xEnd,
                            numpyGrid, drawNumber)

        # Put houses on grid and calculate score
        else:

            # Update uniqueID and place houses on numpy grid
            currentObject.uniqueID = 10 + object
            placeOnGrid(currentObject, numpyGrid)

    # After placing all houses, loop over them
    for object in range(len(residentialArea)):

        # Give the current object an easy variable
        currentObject = residentialArea[object]

        # Calculate score if current item is not water
        if currentObject.type != "water":

            # Find all extra free area per house per step of 2 meter
            increase = (1 * 2)

            # Create a numpyGrid copy
            numpyGridOriginal = numpyGrid

            # For each house, calculate its extra free area
            checkAllFreeArea(currentObject, increase, numpyGrid,
                             numpyGridOriginal)

            # Then, calculate the new value of each house
            currentResult["score"] += currentObject.calculateScore()

    return residentialArea, numpyGrid, currentResult

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

    # Extract object dimension (x, y tuple) values
    objectYLength = currentObject.objectDimensions[1]
    objectXLength = currentObject.objectDimensions[0]

    # Define end coordinates (y, x tuple)
    endCoordinates = (coordinates[0] + objectYLength,
                      coordinates[1] + objectXLength)

    # Update coordinates
    currentObject.yBegin = coordinates[0]
    currentObject.yEnd = endCoordinates[0]
    currentObject.xBegin = coordinates[1]
    currentObject.xEnd = endCoordinates[1]

def coordinateVariables(currentObject):

    # Define coordinate variables
    yBegin = currentObject.yBegin
    yEnd = currentObject.yEnd
    xBegin = currentObject.xBegin
    xEnd = currentObject.xEnd
    freeArea = currentObject.freeArea

    # Define (coordinate incl. free area) variables
    fAYBegin = yBegin - freeArea
    fAYEnd = yEnd + freeArea
    fAXBegin = xBegin - freeArea
    fAXEnd = xEnd + freeArea

    return yBegin, yEnd, xBegin, xEnd, freeArea, fAYBegin, fAYEnd, fAXBegin, fAXEnd

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

    # Get coordinate variables
    coord = coordinateVariables(currentObject)

    # Specify drawNumbers
    drawNumber = currentObject.uniqueID
    fADrawNumber = 1

    # Check for grid border problems
    if currentObject.checkBorders() == True:

        # Check for house and free area overlap
        if \
        checkOverlap(coord[0], coord[1], coord[2], coord[3],
                    numpyGrid, "excludingFreeArea") == True and \
        checkOverlap(coord[5], coord[6], coord[7], coord[8],
                    numpyGrid, "includingFreeArea") == True:

            # The area is viable: draw free area first
            visualizeOnGrid(coord[5], coord[6], coord[7], coord[8],
                            numpyGrid, fADrawNumber)

            # Visualize house on top of free area
            visualizeOnGrid(coord[0], coord[1], coord[2], coord[3],
                            numpyGrid, drawNumber)

        # Start over, because there are house and/or free area overlap issues
        else:
            placeOnGrid(currentObject, numpyGrid)

    # Start over, because the house is overlining the border
    else:
        placeOnGrid(currentObject, numpyGrid)

def visualizeOnGrid(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, drawNumber):

    # Select a specific grid area and fill it
    numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] = drawNumber

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

    # Remove all (increase) modifications before (re)starting
    numpyGrid = numpyGridOriginal

    # Get coordinate variables
    coord = coordinateVariables(currentObject)

    # Specify drawNumbers
    drawNumber = currentObject.uniqueID
    fADrawNumber = 1

    # Change uniqueID drawnumber to 1's for this method to work
    numpyGrid[coord[0]:coord[1],coord[2]:coord[3]] = fADrawNumber

    # Check if new area contains only empty-values or free area-values
    if \
    np.all(numpyGrid[coord[5] - increase:coord[6] + increase,
    coord[7] - increase:coord[8] + increase] <= 1) and \
    currentObject.checkBorders() == True:

        # Update extra free area in self
        currentObject.extraFreeArea = increase

        # Increase X, Y and call self until impossible
        increase += (1 * 2)
        checkAllFreeArea(currentObject, increase, numpyGrid, numpyGridOriginal)

    else:

        # Re-draw number, because we deleted it a few steps ago
        numpyGrid[coord[0]:coord[1],coord[2]:coord[3]] = drawNumber

        # Remove all other modifications before ending
        numpyGrid = numpyGridOriginal

        return False

def hillVisualizer(currentObject, numpyGrid):

    # if currentObject.type == "eengezinswoning":
    #     currentObject.freeArea = 2 * 2
    # elif currentObject.type == "bungalow":
    #     currentObject.freeArea = 3 * 2
    # elif currentObject.type == "maison":
    #     currentObject.freeArea = 6 * 2

    # Get coordinate variables
    coord = coordinateVariables(currentObject)

    # Specify drawNumbers
    drawNumber = currentObject.uniqueID
    fADrawNumber = 1

    # The area is viable: draw free area first
    visualizeOnGrid(coord[5], coord[6], coord[7], coord[8],
                    numpyGrid, fADrawNumber)

    # Visualize house on top of free area
    visualizeOnGrid(coord[0], coord[1], coord[2], coord[3],
                    numpyGrid, drawNumber)

def fixIncorrectVisualizations(currentObject, numpyGrid):

    # if currentObject.type == "eengezinswoning":
    #     currentObject.freeArea = 2 * 2
    # elif currentObject.type == "bungalow":
    #     currentObject.freeArea = 3 * 2
    # elif currentObject.type == "maison":
    #     currentObject.freeArea = 6 * 2

    # Get coordinate variables
    coord = coordinateVariables(currentObject)

    # Specify drawNumbers
    drawNumber = currentObject.uniqueID
    fADrawNumber = 1

    # The area is viable: draw free area first
    visualizeOnGrid(coord[5], coord[6], coord[7], coord[8],
                    numpyGrid, fADrawNumber)

    # Visualize house on top of free area
    visualizeOnGrid(coord[0], coord[1], coord[2], coord[3],
                    numpyGrid, drawNumber)

def getVideo(residentialArea):

    # Get video output
    for indexPhoto in range(len(residentialArea)):
        GIFPlot(residentialArea, indexPhoto)
        indexPhoto += 1

    # Create video output
    os.system("ffmpeg -framerate 1/0.15 -i tmp/%03d.png "+
    "-c:v libx264 -r 30 tmp/__output.mp4")

def GIFPlot(residentialArea, indexPhoto):

    # Initialize matplotlib and figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Display score
    newScore = 0

    # Loop over all objects
    for object in residentialArea[0:indexPhoto+1]:

        # Update score
        if object.type != "water":
            currentScore = object.calculateScore()
            newScore += currentScore

        # Draw water, houses and free area
        drawPlotObjects(residentialArea, object, ax)

    # Add current score title
    plt.title(str(newScore) + " euro")

    # Set figure dimensions
    plt.xlim([0, gridXLength])
    plt.ylim([0, gridYLength])

    # Save pic
    pictureName = '{:03}'.format(indexPhoto)
    plt.savefig('tmp/'+pictureName, dpi=200, bbox_inches='tight')
    plt.close(fig)

def printPlot(allResults):

    residentialArea = allResults["highestScoreMap"]
    totalScore = allResults["highestScore"]

    # Initialize matplotlib and figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Add score title
    plt.title(str(totalScore) + " euro")

    # Loop over all objects
    for object in residentialArea:

        # Draw water, houses and free area
        drawPlotObjects(residentialArea, object, ax)

    # Set figure dimensions
    plt.xlim([0, gridXLength])
    plt.ylim([0, gridYLength])

    # Show matplotlib
    plt.show()
    plt.close(fig)

def drawPlotObjects(residentialArea, object, ax):

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

def updateResults(currentResult, allResults):

    # Update all results
    allResults["allScores"] += currentResult["score"]
    allResults["allRuntimes"] += currentResult["runtime"]

    # Update avg results
    allResults["averageScore"] = int((allResults["allScores"]/allResults["rounds"]))
    allResults["averageRuntime"] = (allResults["allRuntimes"]/allResults["rounds"])

    # Update score results
    if currentResult["score"] > allResults["highestScore"]:
        allResults["highestScore"] = 0
        allResults["highestScore"] = currentResult["score"]
        allResults["highestScoreMap"] = currentResult["residentialArea"]

    if currentResult["score"] < allResults["lowestScore"]:
        allResults["lowestScore"] = 0
        allResults["lowestScore"] = currentResult["score"]

    # Update runtime results
    if currentResult["runtime"] < allResults["fastestRuntime"]:
        allResults["fastestRuntime"] = 0
        allResults["fastestRuntime"] = currentResult["runtime"]

    if currentResult["runtime"] > allResults["slowestRuntime"]:
        allResults["slowestRuntime"] = 0
        allResults["slowestRuntime"] = currentResult["runtime"]

    return allResults
