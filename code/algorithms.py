import glob
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import os
import random as rd
import sys
from functions import *
from models.models import *
from models.templates import *
from timeit import default_timer as timer

def hillyAlgorithm():

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
    hillyResult = Results(**resultsTemplate)

    maxEengezinshuizenOnRow = 15
    maxBungalowsOnRow = 2
    laneCounters = [0, 0, 0, maxEengezinshuizenOnRow, maxBungalowsOnRow]

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

            # Update uniqueID
            currentObject.uniqueID = 10 + object

            if currentObject.type == "eengezinswoning":

                dimensions = (currentObject.objectDimensions[0] + (currentObject.freeArea * 2))
                fixOnGrid(currentObject, numpyGrid, dimensions, laneCounters)
                laneCounters[0] += 1

                if laneCounters[0] > maxEengezinshuizenOnRow:
                    laneCounters[1] += 1

                if laneCounters[1] > maxEengezinshuizenOnRow:
                    laneCounters[2] += 1

            # Place houses on numpy grid
            else:
                print("other house, bitch")
                #placeOnGrid(currentObject, numpyGrid)

    # Loop over all objects (water + houses)
    for object in range(len(residentialArea)):

        # Give the current object an easy variable
        currentObject = residentialArea[object]

        # Put other houses on numpy grid
        if currentObject.type == "water" or currentObject.type == "eengezinswoning":
            print("no")
        else:
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
            hillyResult.highestScore += currentObject.calculateScore()

    # Save current results
    hillyResult.maxHouses = maxHouses
    hillyResult.highestScoreMap = residentialArea
    hillyResult.numpyGrid = numpyGrid

    #printPlot(currentResult)
    return hillyResult

def fixOnGrid(currentObject, numpyGrid, dimensions, laneCounters):

    # Specify drawNumbers
    drawNumber = currentObject.uniqueID
    fADrawNumber = 1

    # Define variables
    maxEengezinshuizenOnRow = laneCounters[3]

    coordinates = (300, currentObject.freeArea + dimensions * laneCounters[0])
    updateCoordinates(currentObject, coordinates)

    # Check for grid border problems
    if currentObject.checkBorders() != True:

        if laneCounters[1] < maxEengezinshuizenOnRow:
            coordinates = (300 - dimensions, currentObject.freeArea + dimensions * laneCounters[1])

        else:
            coordinates = (300 - dimensions * 2, currentObject.freeArea + dimensions * laneCounters[2])

        updateCoordinates(currentObject, coordinates)

    # Get coordinate variables
    coord = coordinateVariables(currentObject)

    # The area is viable: draw free area first
    visualizeOnGrid(coord[5], coord[6], coord[7], coord[8],
                    numpyGrid, fADrawNumber)

    # Visualize house on top of free area
    visualizeOnGrid(coord[0], coord[1], coord[2], coord[3],
                    numpyGrid, drawNumber)

def visualizeOnGrid(newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid, drawNumber):

    # Select a specific grid area and fill it
    numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] = drawNumber

# Run random algorithm
def randomAlgorithm(randomResults):

    # Update round
    randomResults.roundsCounter += 1

    # Remove old output results
    for png in glob.glob("tmp/*.png"):
        os.remove(png)

    for mp4 in glob.glob("tmp/*.mp4"):
        os.remove(mp4)

    # Measure algorithm time
    timeStart = timer()

    # Get a random map and its results
    currentResult = initializeRandomMap()

    # Update algorithm runtimes
    timeEnd = timer()
    runtime = (timeEnd - timeStart)
    currentResult.fastestRuntime = runtime
    randomResults.totalRuntime += runtime

    # Based on the current results, check for higher/lower scores and update
    randomResults = updateResults(currentResult, randomResults)

    # Print current score and total runtime
    runtimeDecimal = "%.3f" % randomResults.totalRuntime
    print("Total runtime (sec.):",
    runtimeDecimal,"|| Score:",currentResult.highestScore,
    "|| Round:",randomResults.roundsCounter)

    # Only run 'rounds' amount of times
    if randomResults.roundsCounter < randomResults.rounds:
        randomAlgorithm(randomResults)

    else:
        # Print high/low score & runtime
        print("")
        print("Rounds:", randomResults.rounds, "|| MaxHouses:", \
        randomResults.maxHouses)
        print("---------------------------------------------")
        print("Highest score:", randomResults.highestScore)
        print("Lowest score:", randomResults.lowestScore)
        print("Average score:", randomResults.averageScore)
        print("---------------------------------------------")
        print("Fastest runtime (sec):", randomResults.fastestRuntime)
        print("Slowest runtime (sec):", randomResults.slowestRuntime)
        print("Average runtime (sec):", randomResults.averageRuntime)
        print("---------------------------------------------")
        print("Total runtime (sec):", randomResults.totalRuntime)
        print("")

        return randomResults

# Run hillclimber algorithm
def hillclimberAlgorithm(hillclimberResults, randomResults):

    # Remove old output results
    for png in glob.glob("tmp/*.png"):
        os.remove(png)

    for mp4 in glob.glob("tmp/*.mp4"):
        os.remove(mp4)

    # Measure algorithm time
    timeStart = timer()

    # Extract map and results
    residentialArea = randomResults.highestScoreMap
    numpyGrid = randomResults.numpyGrid

    # Define score to compare against
    oldScore = randomResults.highestScore

    # Do hillclimber x amount of times
    hillclimberCore(hillclimberResults, residentialArea,
                    numpyGrid, oldScore)

    # Update algorithm runtime
    timeEnd = timer()
    runtime = (timeEnd - timeStart)

    # Print runtime
    print("")
    print("Rounds:",int(hillclimberResults.rounds))
    print("Total elapsed time (in seconds):",runtime)
    print("Total swaps:",hillclimberResults.swaps)
    print("")

    # Visualize grid with matplotlib
    printPlot(hillclimberResults)

def hillclimberCore(hillclimberResults, residentialArea, numpyGrid, oldScore):

    # Update round
    hillclimberResults.roundsCounter += 1

    # Only run 'rounds' amount of times
    if hillclimberResults.roundsCounter < hillclimberResults.rounds:

        # Pick random houses & update new coordinates
        results = switchCoordinates(residentialArea, numpyGrid)
        randomHouse1 = results[0]
        randomHouse2 = results[1]
        oldCoordinates1 = results[2]
        oldCoordinates2 = results[3]

        # Check restrictions
        if \
        checkAvailableArea(randomHouse1, numpyGrid, residentialArea) == True and \
        checkAvailableArea(randomHouse2, numpyGrid, residentialArea) == True:

            # Place houses on numpyGrid
            placeOnHillGrid(randomHouse1, numpyGrid)
            placeOnHillGrid(randomHouse2, numpyGrid)

            # Initialize the score of this round
            newScore = 0

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

                # Then, calculate the new value of each house
                newScore += currentObject.calculateScore()

            # If the score is higher, leave the houses on their new spot!
            if newScore > oldScore:

                print("++ Score:", newScore, "vs.", oldScore, "|| Round:",
                hillclimberResults.roundsCounter)

                # Update scores
                hillclimberResults.highestScore = newScore
                hillclimberResults.highestScoreMap = residentialArea
                hillclimberResults.swaps += 1

                # Update score to compare against
                oldScore = newScore

                # Run hillclimber again
                hillclimberCore(hillclimberResults, residentialArea,
                                numpyGrid, oldScore)

            # Else, score is lower
            else:

                print("-- Score:", newScore, "vs.", oldScore, "|| Round:",
                hillclimberResults.roundsCounter)

                # Revert to old coordinates and fix numpyGrid
                revertSituation(randomHouse1, randomHouse2, oldCoordinates1,
                                oldCoordinates2, numpyGrid, residentialArea)

                # Re-calculate extra free area for this old situation
                recalculateAllExtraFreeArea(residentialArea, numpyGrid)

                # Run hillclimber again
                hillclimberCore(hillclimberResults, residentialArea,
                                numpyGrid, oldScore)

        else:

            # Revert to old coordinates and fix numpyGrid
            revertSituation(randomHouse1, randomHouse2, oldCoordinates1,
                            oldCoordinates2, numpyGrid, residentialArea)

            # Re-calculate extra free area for this old situation
            recalculateAllExtraFreeArea(residentialArea, numpyGrid)

            # Run hillclimber again
            hillclimberCore(hillclimberResults, residentialArea,
                            numpyGrid, oldScore)

    else:
        return hillclimberResults
