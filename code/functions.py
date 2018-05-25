import csv
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

def initializeRandomMap():
    """
    This function creates a random residential area with 20, 40 or 60 houses
    places. It calculates the corresponding score.
    The function returns the map, score, and performance.
    """

    # Measure algorithm time
    timeStart = timer()

    # Set-up residentialArea
    results = setUpResidentialAreaPlusGrid()
    residentialArea = results[0]
    numpyGrid = results[1]
    maxHouses = results[2]

    # Initialize current score
    currentResult = Results(**resultsTemplate)

    # Loop over all objects (water + houses)
    for object in range(len(residentialArea)):

        # Give the current object an easy variable
        currentObject = residentialArea[object]

        # Put water on numpy grid
        if currentObject.type == "water":

            # Set its coordinates and update uniqueID
            changeCoordinates(currentObject, (0, 0))
            currentObject.uniqueID = 200

            # Define the number in the numpy grid
            drawNumber = 3

            # Immediately plot it, as the field is empty at the moment
            visualizeOnGrid(currentObject.yBegin, currentObject.yEnd,
                            currentObject.xBegin, currentObject.xEnd,
                            numpyGrid, drawNumber)
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
            currentResult.highestScore += currentObject.calculateScore()

    # Update algorithm runtimes
    timeEnd = timer()
    runtime = (timeEnd - timeStart)

    # Save current results
    currentResult.maxHouses = maxHouses
    currentResult.highestScoreMap = residentialArea
    currentResult.numpyGrid = numpyGrid
    currentResult.totalRuntime = runtime

    return currentResult

def setUpResidentialAreaPlusGrid():
    """
    This function creates an array for the residential area and places
    the defined amount of houses within the array on the grid.
    The function returns the residential area, numpy grid, and #houses.
    """

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
    numpyGrid = np.zeros((gridYLength,gridXLength), dtype="object")

    return residentialArea, numpyGrid, maxHouses

# Define residential area size (either 20, 40 or 60 houses at max)
def defineSettings():
    """
    This function sets and returns the amount of houses in the residential area.
    The amount depends on the user input and if the user does not input
    a valid number, the function will set 20 houses by default.
    """

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

def getRandomCoordinates(currentObject):
    """
    This function generates random coordinates for the current object in the
    residential area and updates it in self.
    """

    # Set new begin coordinates (y, x tuple) and save them in self
    currentObject.yBegin = rd.randrange(currentObject.gridYLength)
    currentObject.xBegin = rd.randrange(currentObject.gridXLength)
    beginCoordinates = (currentObject.yBegin, currentObject.xBegin)

    # Update end coordinates
    changeCoordinates(currentObject, beginCoordinates)

def changeCoordinates(currentObject, coordinates):
    """
    This function updates the given (y, x) coordinates in self.
    """

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
    """
    This function grabs the coordinates, adds the minimum free area and
    returns all the variables.
    """

    # Define coordinate variables
    yBegin = currentObject.yBegin
    yEnd = currentObject.yEnd
    xBegin = currentObject.xBegin
    xEnd = currentObject.xEnd
    freeArea = currentObject.freeArea

    # Define coordinate variables including free area
    fAYBegin = yBegin - freeArea
    fAYEnd = yEnd + freeArea
    fAXBegin = xBegin - freeArea
    fAXEnd = xEnd + freeArea

    return yBegin, yEnd, xBegin, xEnd, freeArea, fAYBegin, fAYEnd, fAXBegin, \
    fAXEnd

def placeOnGrid(currentObject, numpyGrid):
    """
    This function places the current object in the residential area on the grid.
    It checks the requirements for overlap and borders.
    """

    # Get random coordinates and update in self
    getRandomCoordinates(currentObject)

    # Get coordinate variables
    coord = coordinateVariables(currentObject)

    # Specify drawNumbers
    drawNumber = currentObject.uniqueID
    fADrawNumber = 1

    # Check for grid border problems
    if currentObject.checkBorders() == True:

        # Check for house and free area overlap
        check1 = checkOverlap(coord[0], coord[1], coord[2], coord[3], \
        numpyGrid, "doNotAllowAnyOverlap")
        check2 = checkOverlap(coord[5], coord[6], coord[7], coord[8], \
        numpyGrid, "allowFreeAreaOverlap")

        if check1 == True and check2 == True:

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

def createhillMovesGrid(currentObject, numpyGrid, dimensions, houseCounter):
    """
    This function creates the specific grid for the hillclimber-moves algorithm.
    """

    YPosition = 300
    waterWidth = int(23040/296)

    # Specify drawNumbers
    drawNumber = currentObject.uniqueID
    fADrawNumber = 1

    # Define the maximum number of houses that can be placed on one row
    maxHousesOnRow = houseCounter[3]

    if currentObject.type == "eengezinswoning":
        maxHousesOnNextRows = houseCounter[4]

        # Put eengezinswoningen on the first row
        if houseCounter[0] < maxHousesOnRow:
            coordinates = (YPosition, currentObject.freeArea
                            + dimensions * houseCounter[0])

        # Put eengezinswoningen on the second row
        elif houseCounter[1] < maxHousesOnNextRows:
            coordinates = (YPosition - dimensions, waterWidth +
            currentObject.freeArea + dimensions * houseCounter[1])

        # Put eengezinswoningen on the third row
        elif houseCounter[2] < maxHousesOnNextRows:
            coordinates = (YPosition - dimensions * 2, waterWidth +
            currentObject.freeArea + dimensions * houseCounter[2])

    else:

        # Put bungalows on the first row
        if houseCounter[0] < maxHousesOnRow:
            coordinates = (currentObject.freeArea,
            waterWidth + currentObject.freeArea + dimensions * \
            houseCounter[0])

        # Put bungalows on the second row
        elif houseCounter[1] < maxHousesOnRow:
            coordinates = (currentObject.freeArea + dimensions,
            waterWidth + currentObject.freeArea + dimensions * \
            houseCounter[1])

        # Put bungalows on the third row
        elif houseCounter[2] < maxHousesOnRow:
            coordinates = (currentObject.freeArea + dimensions * 2,
            waterWidth + currentObject.freeArea + dimensions * \
            houseCounter[2])

    # Update coordinats in self
    changeCoordinates(currentObject, coordinates)

    # Get coordinate variables
    coord = coordinateVariables(currentObject)

    # The area is clear, so we can immediately draw the free area
    visualizeOnGrid(coord[5], coord[6], coord[7], coord[8],
                    numpyGrid, fADrawNumber)

    # Visualize house on top of free area
    visualizeOnGrid(coord[0], coord[1], coord[2], coord[3],
                    numpyGrid, drawNumber)

def visualizeOnGrid(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, \
    drawNumber):
    """
    This function selects a specific area on the numpy grid, and fills that
    with the specified drawNumber.
    """

    # Select a specific grid area and fill it
    numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] = drawNumber

def checkOverlap(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, choice):
    """
    This function checks whether a certain area is clear (EVERY value in the
    numpy grid should be 0), or allows free area overlap (ALL values in the
    numpy grid should be 0 or 1). It returns True or False,
    depending on the result.
    """

    # Every value in the grid should be 0, which means it is empty
    if choice == "doNotAllowAnyOverlap":

        # Check house area if it's completely empty
        if np.any(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] != 0):
            return False

        else:
            return True

    # Check whether this area is completely clear (0) or contains free area (1)
    if choice == "allowFreeAreaOverlap":
        if np.all(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] <= 1):
            return True

        else:
            return False

def recalculateAllExtraFreeArea(residentialArea, numpyGrid):
    """
    This function loops over all houses in the residential area, removes old
    worth, and calculates the new extra free area.
    """

    # After placing all houses, loop over them
    residentialAreaNew = residentialArea[1:len(residentialArea)]
    for object in range(len(residentialAreaNew)):

        # Give the current object an easy variable
        currentObject = residentialAreaNew[object]

        # Remove old value to avoid unexpected overlap
        currentObject.extraFreeArea = 0

        # Find all extra free area per house
        increase = (1 * 2)
        numpyGridOriginal = numpyGrid
        checkAllFreeArea(currentObject, increase, numpyGrid,
                         numpyGridOriginal)

def checkAllFreeArea(currentObject, increase, numpyGrid, numpyGridOriginal):
    """
    This function takes the numpy grid, selects a specific house area and
    increases that area each time this function is called. That widened area
    must not overlap other houses, but it is allowed to have free area overlap.
    By doing this, the maximum amount of free area is calculated.
    """

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

        return False

def getHouse(residentialArea):
    """
    This function selects a random house from the residential area.
    It returns the chosen house.
    """

    # Select and return a random house
    oneRandomHouse = residentialArea[rd.randrange(len(residentialArea))]

    return oneRandomHouse

def switchCoordinates(residentialArea, numpyGrid):
    """
    This function randomly selects two unique houses from the residential area
    that are not of the same type, swaps their coordinates and updates those
    in self. It returns the two houses and their old coordinates.
    """

    # Get residentialArea without water (avoiding problems)
    residentialAreaNew = residentialArea[1:len(residentialArea)]

    # Select random house
    randomHouse1 = residentialAreaNew[rd.randrange(len(residentialAreaNew))]
    randomHouse2 = residentialAreaNew[rd.randrange(len(residentialAreaNew))]

    # Retry if both houses are the same or are the same type
    while \
    randomHouse1.uniqueID == randomHouse2.uniqueID or \
    randomHouse1.type == randomHouse2.type:

        # Select random house again
        randomHouse1 = residentialAreaNew[rd.randrange(len(residentialAreaNew))]
        randomHouse2 = residentialAreaNew[rd.randrange(len(residentialAreaNew))]
        break

    # Save old and new coordinates
    oldCoordinates1 = (randomHouse1.yBegin, randomHouse1.xBegin)
    oldCoordinates2 = (randomHouse2.yBegin, randomHouse2.xBegin)
    newCoordinates1 = (randomHouse2.yBegin, randomHouse2.xBegin)
    newCoordinates2 = (randomHouse1.yBegin, randomHouse1.xBegin)

    # Remove houses from map and numpyGrid
    randomHouse1.removeFromGridAndMap(numpyGrid)
    randomHouse2.removeFromGridAndMap(numpyGrid)

    # Fix rough free area removal
    redrawGrid(residentialArea, numpyGrid)

    # Update coordinates
    changeCoordinates(randomHouse1, newCoordinates1)
    changeCoordinates(randomHouse2, newCoordinates2)

    # Return valid random selected houses
    return randomHouse1, randomHouse2, oldCoordinates1, oldCoordinates2

def checkAvailableArea(currentObject, numpyGrid, residentialArea):
    """
    This function checks whether the current house (with newly updated
    coordinates) can be placed on the grid and not cause overlap issues.
    It returns True or False, depending on the result.
    """

    # Get coordinate variables
    coord = coordinateVariables(currentObject)

    # Check for grid border problems
    if currentObject.checkBorders() == True:

        # Check for house and free area overlap
        if \
        checkOverlap(coord[0], coord[1], coord[2], coord[3], numpyGrid,
                    "doNotAllowAnyOverlap") == True and \
        checkOverlap(coord[5], coord[6], coord[7], coord[8], numpyGrid,
                    "allowFreeAreaOverlap") == True:

            return True

        # Start over, because there are house and/or free area overlap issues
        else:
            return False

    # Start over, because the house is overlining the border
    else:
        return False

def placeOnHillGrid(currentObject, numpyGrid):
    """
    This function draws the free area and house on the numpy grid.
    """

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

def redrawGrid(residentialArea, numpyGrid):
    """
    This function loops over all objects and re-draws the free area, the
    house, and water on the numpy grid. Missing free area values in the numpy
    grid (which happens after removing an other house from the grid) will be
    restored.
    """

    # Re-draw water
    waterObject = residentialArea[0]
    coord = coordinateVariables(waterObject)
    drawNumber = 3
    visualizeOnGrid(coord[0], coord[1], coord[2], coord[3],
                    numpyGrid, drawNumber)

    # Create list without water to avoid problems
    residentialAreaNew = residentialArea[1:len(residentialArea)]

    # Loop over all houses
    for object in range(len(residentialAreaNew)):

        # Give the current object an easy variable
        currentObject = residentialAreaNew[object]

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

def revertSingleHouse(randomHouse, oldCoordinates, residentialArea, numpyGrid):
    """
    This function removes the selected house from the numpy grid and map,
    restores its old coordinates, fixes any missing free area because of the
    removal, and recalculates the extra free area.
    """

    # Remove houses from numpyGrid and map
    randomHouse.removeFromGridAndMap(numpyGrid)

    # Revert to old coordinates
    changeCoordinates(randomHouse, oldCoordinates)

    # Clean-up some bugs and plot old location back
    redrawGrid(residentialArea, numpyGrid)

    # Re-calculate extra free area for this old situation
    recalculateAllExtraFreeArea(residentialArea, numpyGrid)

def deleteOldImages():
    """
    This function removes the visualization images.
    """

    # Remove all .png's
    for png in glob.glob("tmp/*.png"):
        os.remove(png)

    # Remove all .mp4's
    for mp4 in glob.glob("tmp/*.mp4"):
        os.remove(mp4)

def getVideo(results, choice):
    """
    This function creates a visualization of the results of the algorithm.
    """

    # Extract variable
    residentialArea = results.highestScoreMap

    # Get video output
    if choice == "random":
        for GIFindex in range(len(residentialArea)):
            matplotlibCore(residentialArea, choice, GIFindex, results)
            GIFindex += 1

    else:
        matplotlibCore(residentialArea, choice, GIFindex, results)

    # Create video output
    FFmpeg()

def FFmpeg():
    """
    This function executes the necessary command to turn pictures into a video.
    """

    os.system("ffmpeg -framerate 1/0.15 -i tmp/%03d.png "+
    "-c:v libx264 -r 30 tmp/__output.mp4")

def matplotlibCore(residentialArea, choice, GIFindex, results):
    """
    This function creates a matplotlib figure of the residential area and
    either shows it, or saves it.
    """

    # Initialize matplotlib and figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if choice == "printPlot":

        # Extract highest score
        score = results.highestScore

        # Loop over all objects
        for object in residentialArea:

            # Draw water, houses and free area
            drawPlotObjects(residentialArea, object, ax)

    else:

        # Get score and visualize houses and water
        score = getPlotObjects(residentialArea, choice, GIFindex, fig, ax)

    # Add score title
    title = results.algorithm + " — " + str(results.maxHouses) + \
    " houses: " + str(score) + " euro"
    plt.title(title)

    # Set figure dimensions
    plt.xlim([0, gridXLength])
    plt.xlabel("width")
    plt.ylim([0, gridYLength])
    plt.ylabel("height")

    if choice == "printPlot":

        # Show matplotlib
        plt.show()

    else:

        # Save pic
        pictureName = "{:03}".format(GIFindex)
        plt.savefig("tmp/"+pictureName, dpi=125, bbox_inches="tight")

    plt.close(fig)

def getPlotObjects(residentialArea, choice, GIFindex, fig, ax):
    """
    This function creates matplotlib objects of water and all houses and
    calculates the score. It returns the score of the residential area.
    """

    # Display score
    newScore = 0

    if choice != "random":

        # Loop over all objects
        for object in residentialArea:

            # Update score
            if object.type != "water":
                currentScore = object.calculateScore()
                newScore += currentScore

            # Draw water, houses and free area
            drawPlotObjects(residentialArea, object, ax)

    else:

        # Loop over index+1 objects
        for object in residentialArea[0:GIFindex+1]:

            # Update score
            if object.type != "water":
                currentScore = object.calculateScore()
                newScore += currentScore

            # Draw water, houses and free area
            drawPlotObjects(residentialArea, object, ax)

    return newScore

def drawPlotObjects(residentialArea, object, ax):
    """
    This function visualizes the dimensions of water and all houses on the map.
    """

    # Initialize variables
    yBegin = object.yBegin
    yEnd = object.yEnd
    xBegin = object.xBegin
    xEnd = object.xEnd
    fA = object.freeArea
    eFA = object.extraFreeArea

    # Define color for free area
    colorChoice = "gray"

    # Define color for house
    if object.type == "eengezinswoning":
        colorChoice2 = "red"

    elif object.type == "bungalow":
        colorChoice2 = "green"

    elif object.type == "maison":
        colorChoice2 = "yellow"

    elif object.type == "water":
        colorChoice2 = "blue"

    # Create new rects for freeArea + house
    rectUpperRight = patches.Rectangle((xBegin,yBegin),            # (X,Y) tuple
                             xEnd - xBegin + fA + eFA,             # width
                             yEnd - yBegin + fA + eFA,             # height
                             color=colorChoice,
                             alpha=0.2)

    rectUpperLeft = patches.Rectangle((xBegin - fA - eFA,yBegin),  # (X,Y) tuple
                             xEnd - xBegin + fA + eFA,             # width
                             yEnd - yBegin + fA + eFA,             # height
                             color=colorChoice,
                             alpha=0.2)

    rectLowerRight = patches.Rectangle((xEnd + fA + eFA,yEnd),     # (X,Y) tuple
                             xBegin - xEnd - fA - eFA,             # width
                             yBegin - yEnd - fA - eFA,             # height
                             color=colorChoice,
                             alpha=0.2)

    rectLowerLeft = patches.Rectangle((xEnd,yEnd),                 # (X,Y) tuple
                             xBegin - xEnd - fA - eFA,             # width
                             yBegin - yEnd - fA - eFA,             # height
                             color=colorChoice,
                             alpha=0.2)

    # Create new rect for house only
    rectHouse = patches.Rectangle((xBegin,yBegin),                 # (X,Y) tuple
                             (xEnd - xBegin),                      # width
                             (yEnd - yBegin),                      # height
                             color=colorChoice2,)

    # Add the rects
    ax.add_patch(rectUpperRight)
    ax.add_patch(rectUpperLeft)
    ax.add_patch(rectLowerRight)
    ax.add_patch(rectLowerLeft)
    ax.add_patch(rectHouse)

def updateResults(currentResult, allResults):
    """
    This function updates the results in its template. It returns the template.
    """

    # Update all results
    allResults.maxHouses = currentResult.maxHouses
    allResults.allScores += currentResult.highestScore
    allResults.totalRuntime += currentResult.totalRuntime

    # Update avg results
    allResults.averageScore = int((allResults.allScores/allResults.rounds))

    # Update score results
    if currentResult.highestScore > allResults.highestScore:
        allResults.highestScore = currentResult.highestScore
        allResults.highestScoreMap = currentResult.highestScoreMap
        allResults.numpyGrid = currentResult.numpyGrid

    if currentResult.highestScore < allResults.lowestScore:
        allResults.lowestScore = currentResult.highestScore

    return allResults

def writeResults(results):
    """
    This function writes the statistics of the algorithm in scores.csv.
    """

    # Open scores.csv
    with open("scores.csv", "a", newline="") as csvfile:
        fieldnames = [
            "algorithm",
            "number of houses",
            "rounds",
            "highest score",
            "lowest score",
            "score difference",
            "swaps",
            "moves",
            "total runtime (sec)"
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Only write headers if file is empty
        if os.stat("scores.csv").st_size == 0:
            writer.writeheader()

        # Write the rest
        writer.writerow({
            "algorithm": results.algorithm,
            "number of houses": results.maxHouses,
            "rounds": results.rounds,
            "highest score": results.highestScore,
            "lowest score": results.lowestScore,
            "score difference": results.scoreDifference,
            "swaps": results.swaps,
            "moves": results.moves,
            "total runtime (sec)": results.totalRuntime
            })
