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

def hillclimberAlgorithm(allResults):
#def hillclimberAlgorithm(randomMap, allResults):

    # Update round
    allResults["roundsCounter"] += 1

    # Remove old output results
    for png in glob.glob("tmp/*.png"):
        os.remove(png)

    for mp4 in glob.glob("tmp/*.mp4"):
        os.remove(mp4)

    # Measure algorithm time
    timeStart = timer()

    # Get maxHouses and update in results sheet
    maxHouses = defineSettings()
    allResults["maxHouses"] = maxHouses

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

    # Initialize total score
    currentResult = {
                    "score": 0,
                    "runtime": 0,
                    "residentialArea": [],
                    }

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

    # Get first score
    oldScore = 0

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
            currentResult["score"] += currentObject.calculateScore()
            oldScore += currentObject.calculateScore()

    # if allResults["roundsCounter"] < allResults["rounds"]:
    #
    #     results = switchCoordinates(residentialArea, numpyGrid)
    #     randomHouse1 = results[0]
    #     randomHouse2 = results[1]
    #     oldCoordinates1 = results[2]
    #     oldCoordinates2 = results[3]
    #
    #     if placeOnGridHill(randomHouse1, numpyGrid, residentialArea) == True and \
    #     placeOnGridHill(randomHouse2, numpyGrid, residentialArea) == True:
    #
    #         #print("Swap is legit")
    #
    #         # Place houses on numpyGrid
    #         hillVisualizer(randomHouse1, numpyGrid)
    #         hillVisualizer(randomHouse2, numpyGrid)
    #
    #         newScore = 0
    #
    #         # After placing all houses, loop over them
    #         for object in range(len(residentialArea)):
    #
    #             # Give the current object an easy variable
    #             currentObject = residentialArea[object]
    #
    #             # Calculate score if current item is not water
    #             if currentObject.type != "water":
    #
    #                 # Find all extra free area per house
    #                 increase = (1 * 2)
    #                 numpyGridOriginal = numpyGrid
    #                 checkAllFreeArea(currentObject, increase, numpyGrid,
    #                                  numpyGridOriginal)
    #
    #                 # Then, calculate the new value of each house
    #                 newScore += currentObject.calculateScore()
    #
    #         # If the score is higher, leave the houses on their new spot!
    #         if newScore > oldScore:
    #
    #             print("++ Score:", newScore, "vs.", oldScore, "|| round:",["roundsCounter"])
    #
    #             # Update scores
    #             allResults["highestScore"] = 0
    #             allResults["highestScore"] = newScore
    #             allResults["highestScoreMap"] = []
    #             allResults["highestScoreMap"] = residentialArea
    #
    #             # Update score to compare against
    #             oldScore = newScore
    #
    #             hillclimberAlgorithm(randomMap, allResults)
    #
    #         # Else, score is lower
    #         else:
    #
    #             print("-- Score:", newScore, "vs.", oldScore, "|| round:",["roundsCounter"])
    #
    #             # Remove houses from numpyGrid and map
    #             randomHouse1.removeFromGridAndMap(numpyGrid)
    #             randomHouse2.removeFromGridAndMap(numpyGrid)
    #
    #             # Update coordinates
    #             updateCoordinates(randomHouse1, oldCoordinates1)
    #             updateCoordinates(randomHouse2, oldCoordinates2)
    #
    #             # Plot old location back
    #             hillVisualizer(randomHouse1, numpyGrid)
    #             hillVisualizer(randomHouse2, numpyGrid)
    #
    #             hillclimberAlgorithm(randomMap, allResults)
    #
    #     else:
    #
    #         # Remove houses from numpyGrid and map
    #         randomHouse1.removeFromGridAndMap(numpyGrid)
    #         randomHouse2.removeFromGridAndMap(numpyGrid)
    #
    #         # Update coordinates
    #         updateCoordinates(randomHouse1, oldCoordinates1)
    #         updateCoordinates(randomHouse2, oldCoordinates2)
    #
    #         # Plot old location back
    #         hillVisualizer(randomHouse1, numpyGrid)
    #         hillVisualizer(randomHouse2, numpyGrid)
    #
    #         hillclimberAlgorithm(randomMap, allResults)

    # Do hillclimber x amount of times
    for i in range(500):

        results = switchCoordinates(residentialArea, numpyGrid)
        randomHouse1 = results[0]
        randomHouse2 = results[1]
        oldCoordinates1 = results[2]
        oldCoordinates2 = results[3]

        if \
        placeOnGridHill(randomHouse1, numpyGrid, residentialArea) == True and \
        placeOnGridHill(randomHouse2, numpyGrid, residentialArea) == True:

            #print("Swap is legit")

            # Place houses on numpyGrid
            hillVisualizer(randomHouse1, numpyGrid)
            hillVisualizer(randomHouse2, numpyGrid)

            newScore = 0

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

                    # Then, calculate the new value of each house
                    newScore += currentObject.calculateScore()

            # If the score is higher, leave the houses on their new spot!
            if newScore > oldScore:

                print("++ Score:", newScore, "vs.", oldScore, "|| round:",i)

                # Update scores
                allResults["highestScore"] = 0
                allResults["highestScore"] = newScore
                allResults["highestScoreMap"] = []
                allResults["highestScoreMap"] = residentialArea

                # Update score to compare against
                oldScore = newScore

            # Else, score is lower
            else:

                print("-- Score:", newScore, "vs.", oldScore, "|| round:",i)

                # Remove houses from numpyGrid and map
                randomHouse1.removeFromGridAndMap(numpyGrid)
                randomHouse2.removeFromGridAndMap(numpyGrid)

                # Clean-up some bugs
                fixIncorrectVisualizations(randomHouse1, numpyGrid)
                fixIncorrectVisualizations(randomHouse2, numpyGrid)

                # Update coordinates
                updateCoordinates(randomHouse1, oldCoordinates1)
                updateCoordinates(randomHouse2, oldCoordinates2)

                # Plot old location back
                hillVisualizer(randomHouse1, numpyGrid)
                hillVisualizer(randomHouse2, numpyGrid)

        else:

            # Remove houses from numpyGrid and map
            randomHouse1.removeFromGridAndMap(numpyGrid)
            randomHouse2.removeFromGridAndMap(numpyGrid)

            # Clean-up some bugs
            fixIncorrectVisualizations(randomHouse1, numpyGrid)
            fixIncorrectVisualizations(randomHouse2, numpyGrid)

            # Update coordinates
            updateCoordinates(randomHouse1, oldCoordinates1)
            updateCoordinates(randomHouse2, oldCoordinates2)

            # Plot old location back
            hillVisualizer(randomHouse1, numpyGrid)
            hillVisualizer(randomHouse2, numpyGrid)

    # # Clean-up some bugs
    # fixIncorrectVisualizations(randomHouse1, numpyGrid)
    # fixIncorrectVisualizations(randomHouse2, numpyGrid)

    # Update algorithm runtime
    timeEnd = timer()
    runtime = (timeEnd - timeStart)

    # Save current results
    currentResult["runtime"] = runtime
    currentResult["residentialArea"] = residentialArea

    # Update all results
    allResults["totalRuntime"] += runtime
    allResults = updateResults(currentResult, allResults)

    # Print runtime
    print("This round (in seconds):",currentResult["runtime"])
    print("Total elapsed time (in seconds):",allResults["totalRuntime"])
    print("")

    # Visualize grid with matplotlib
    printPlot(allResults)

def switchCoordinates(residentialArea, numpyGrid):

    # Get residentialArea without water (avoiding problems)
    residentialAreaNew = residentialArea[1:len(residentialArea)]

    # Select random house
    randomHouse1 = residentialAreaNew[rd.randrange(len(residentialAreaNew))]
    randomHouse2 = residentialAreaNew[rd.randrange(len(residentialAreaNew))]

    # Retry if selected house is 'water', or when both houses are the same
    # or have the same type
    while \
    randomHouse1.type == "water" or \
    randomHouse2.type == "water" or \
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

    # Loop over all objects (water + houses)
    for object in range(len(residentialArea)):

        # Give the current object an easy variable
        currentObject = residentialArea[object]

        # Fix rough free area removal
        if currentObject.type != "water":
            fixIncorrectVisualizations(currentObject, numpyGrid)

    # Update coordinates
    updateCoordinates(randomHouse1, newCoordinates1)
    updateCoordinates(randomHouse2, newCoordinates2)

    # Return valid random selected houses
    return randomHouse1, randomHouse2, oldCoordinates1, oldCoordinates2

def placeOnGridHill(currentObject, numpyGrid, residentialArea):

    # Get coordinate variables
    coord = coordinateVariables(currentObject)

    # Specify drawNumbers
    drawNumber = currentObject.uniqueID
    fADrawNumber = 1

    # Check for grid border problems
    if currentObject.checkBorders() == True:

        # Check for house and free area overlap
        if \
        checkOverlap(coord[0], coord[1], coord[2], coord[3], numpyGrid,
                        "excludingFreeArea") == True and \
        checkOverlap(coord[5], coord[6], coord[7], coord[8], numpyGrid,
                    "includingFreeArea") == True:

            # # The area is viable: draw free area first
            # visualizeOnGrid(coord[5], coord[6], coord[7], coord[8],
            #                 numpyGrid, fADrawNumber)
            #
            # # Visualize house on top of free area
            # visualizeOnGrid(coord[0], coord[1], coord[2], coord[3],
            #                   numpyGrid, drawNumber)

            return True

        # Start over, because there are house and/or free area overlap issues
        else:

            return False

    # Start over, because the house is overlining the border
    else:

        return False
