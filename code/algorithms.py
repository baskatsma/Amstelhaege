# Authors:
# Amy van der Gun (10791760)
# Bas Katsma (10787690)
# Felicia van Gastel (11096187)
#
# Amstelhaege
# Programmeertheorie
#
# algorithms.py
# File that contains the algorithms used to make the maps, called by main.py

import math
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

# Run random algorithm
def randomAlgorithm(randomResults):
    """
    This algorithm creates a random solution to organize a residential area.
    """

    # Update results sheet
    randomResults.algorithm = "random"

    # Remove old output results
    deleteOldImages()

    # Get a random map and its results
    currentResult = initializeRandomMap()

    # Based on the current results, check for higher/lower scores and update
    randomResults = updateResults(currentResult, randomResults)

    # Print current score and total runtime
    runtimeDecimal = "%.3f" % randomResults.totalRuntime
    print("Total runtime (sec):",
    runtimeDecimal,"|| Score:",currentResult.highestScore,
    "|| Round:",randomResults.roundsCounter)

    # Only run "rounds" amount of times
    randomResults.roundsCounter += 1
    if randomResults.roundsCounter < randomResults.rounds:
        randomAlgorithm(randomResults)

    else:

        # Update scores
        randomResults.scoreDifference = (randomResults.highestScore - \
        randomResults.lowestScore)

        # Print high/low score & runtime
        print("")
        print("Rounds:", randomResults.rounds, "|| MaxHouses:", \
        randomResults.maxHouses)
        print("---------------------------------------------")
        print("Highest score:", randomResults.highestScore)
        print("Lowest score:", randomResults.lowestScore)
        print("Score difference:", randomResults.scoreDifference)
        print("---------------------------------------------")
        print("Total runtime (sec):", randomResults.totalRuntime)
        print("")

    return randomResults

# Run hillSwaps algorithm
def hillSwapsAlgorithm(hillSwapsResults, randomResults):
    """
    This algorithm creates an hillclimber solution to organize a
    residential area.
    """

    # Measure algorithm time
    timeStart = timer()

    # Update template
    hillSwapsResults.algorithm = "hillSwaps"
    hillSwapsResults.maxHouses = randomResults.maxHouses
    hillSwapsResults.lowestScore = randomResults.highestScore
    hillSwapsResults.highestScoreMap = randomResults.highestScoreMap
    hillSwapsResults.numpyGrid = randomResults.numpyGrid
    hillSwapsResults.totalRuntime = randomResults.totalRuntime

    # Remove old output results
    deleteOldImages()

    # Extract result
    oldScore = randomResults.highestScore

    # Do hillSwaps "rounds" amount of times
    hillSwapsCore(hillSwapsResults, oldScore)

    # Update algorithm runtime
    timeEnd = timer()
    runtime = (timeEnd - timeStart)
    hillSwapsResults.totalRuntime += runtime

    # Update scores
    hillSwapsResults.scoreDifference = (hillSwapsResults.highestScore - \
    hillSwapsResults.lowestScore)

    # Print high/low score & runtime
    print("")
    print("Rounds:", hillSwapsResults.rounds, "|| MaxHouses:", \
    hillSwapsResults.maxHouses)
    print("---------------------------------------------")
    print("Total swaps:",int(hillSwapsResults.swaps))
    print("---------------------------------------------")
    print("Highest score:", hillSwapsResults.highestScore)
    print("Lowest score:", hillSwapsResults.lowestScore)
    print("Score difference:", hillSwapsResults.scoreDifference)
    print("---------------------------------------------")
    print("Total runtime (sec):", hillSwapsResults.totalRuntime)
    print("")

    return hillSwapsResults

def hillSwapsCore(hillSwapsResults, oldScore):
    """
    This function picks two random houses, swaps their coordinates, and
    validates whether this is a legit swap. It calculates the score and if it is
    higher, the swap will not revert. It returns the results of the run.
    """

    # Extract map and grid
    residentialArea = hillSwapsResults.highestScoreMap
    numpyGrid = hillSwapsResults.numpyGrid

    # Update round
    hillSwapsResults.roundsCounter += 1

    # Only run "rounds" amount of times
    if hillSwapsResults.roundsCounter <= hillSwapsResults.rounds:

        # Pick random houses & update new coordinates
        results = switchCoordinates(residentialArea, numpyGrid)
        randomHouse1 = results[0]
        randomHouse2 = results[1]
        oldCoordinates1 = results[2]
        oldCoordinates2 = results[3]

        check1 = checkAvailableArea(randomHouse1, numpyGrid, residentialArea)
        check2 = checkAvailableArea(randomHouse2, numpyGrid, residentialArea)

        # Check restrictions
        if check1 == True and check2 == True:

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
                hillSwapsResults.roundsCounter)

                # Update scores
                hillSwapsResults.highestScore = newScore
                hillSwapsResults.highestScoreMap = residentialArea
                hillSwapsResults.numpyGrid = numpyGrid
                hillSwapsResults.swaps += 1

                # Update score to compare against
                oldScore = newScore

                # Create image of current map
                if hillSwapsResults.FFmpegChoice == 1:
                    createImage("hillSwaps", residentialArea, hillSwapsResults)

                # Run hillSwaps again
                hillSwapsCore(hillSwapsResults, oldScore)

            # Else, score is lower
            else:

                print("   Score:", newScore, "vs.", oldScore, "|| Round:",
                hillSwapsResults.roundsCounter)

                # Revert to old coordinates and fix numpyGrid
                revertSingleHouse(randomHouse1, oldCoordinates1,
                residentialArea, numpyGrid)
                revertSingleHouse(randomHouse2, oldCoordinates2,
                residentialArea, numpyGrid)

                # Run hillSwaps again
                hillSwapsCore(hillSwapsResults, oldScore)

        else:

            # Revert to old coordinates and fix numpyGrid
            revertSingleHouse(randomHouse1, oldCoordinates1, residentialArea,
            numpyGrid)
            revertSingleHouse(randomHouse2, oldCoordinates2, residentialArea,
            numpyGrid)

            # Run hillSwaps again
            hillSwapsCore(hillSwapsResults, oldScore)

    else:

        return hillSwapsResults

def hillMovesAlgorithm(hillMovesResults, choice):
    """
    This algorithm creates an heuristic hillclimber solution to organize a
    residential area.
    """

    # Measure algorithm time
    timeStart = timer()

    # Set-up residentialArea
    results = setUpResidentialAreaPlusGrid()
    residentialArea = results[0]
    numpyGrid = results[1]
    maxHouses = results[2]

    # Define variables
    maxEengezinshuizenOnFirstRow = 17
    maxEengezinshuizenOnNextRows = 13
    maxBungalowsOnRow = 10
    eengzRowCounters = [0, 0, 0,
                        maxEengezinshuizenOnFirstRow,
                        maxEengezinshuizenOnNextRows]
    bungaRowCounters = [0, 0, 0,
                        maxBungalowsOnRow]

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

        # Put houses on grid and calculate score
        else:

            # Update uniqueID
            currentObject.uniqueID = 10 + object

            # Place eengezinswoningen
            if currentObject.type == "eengezinswoning":

                dimensions = (currentObject.objectDimensions[0]
                            + currentObject.freeArea)
                createhillMovesGrid(currentObject, numpyGrid,
                                dimensions, eengzRowCounters)
                eengzRowCounters[0] += 1

                if eengzRowCounters[0] > maxEengezinshuizenOnFirstRow:
                    eengzRowCounters[1] += 1

                if eengzRowCounters[1] > maxEengezinshuizenOnNextRows:
                    eengzRowCounters[2] += 1

            # Place bungalows
            elif currentObject.type == "bungalow":

                dimensions = (currentObject.objectDimensions[0]
                            + currentObject.freeArea)
                createhillMovesGrid(currentObject, numpyGrid,
                                dimensions, bungaRowCounters)
                bungaRowCounters[0] += 1

                if bungaRowCounters[0] > maxBungalowsOnRow:
                    bungaRowCounters[1] += 1

                if bungaRowCounters[1] > maxBungalowsOnRow:
                    bungaRowCounters[2] += 1

                if bungaRowCounters[2] > maxBungalowsOnRow:
                    bungaRowCounters[3] += 1

    # Put maisons on numpy grid
    for object in range(len(residentialArea)):
        currentObject = residentialArea[object]

        if currentObject.type == "maison":
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

            # ONLY check maisons, because the rest is locked in as fuck
            if currentObject.type == "maison":
                checkAllFreeArea(currentObject, increase, numpyGrid,
                                numpyGridOriginal)

            # Then, calculate the new value of each house
            hillMovesResults.highestScore += currentObject.calculateScore()

    # Save current results
    hillMovesResults.lowestScore = hillMovesResults.highestScore
    hillMovesResults.maxHouses = maxHouses
    hillMovesResults.highestScoreMap = residentialArea
    hillMovesResults.currentScoreMap = hillMovesResults.highestScoreMap
    hillMovesResults.numpyGrid = numpyGrid

    # Define score to compare against
    oldScore = hillMovesResults.highestScore

    if choice == "hillMoves":

        # Update template
        hillMovesResults.algorithm = "hillMoves"
        hillMovesCore(hillMovesResults, oldScore)

    elif choice == "simAnnealing":

        # Update template
        hillMovesResults.algorithm = "simAnnealing"
        simAnnealing(hillMovesResults, oldScore)

    # Update runtime
    timeEnd = timer()
    runtime = (timeEnd - timeStart)
    hillMovesResults.totalRuntime = runtime

    # Update scores
    hillMovesResults.scoreDifference = (hillMovesResults.highestScore - \
    hillMovesResults.lowestScore)

    # Print high/low score & runtime
    print("")
    print("Rounds:", hillMovesResults.rounds, "|| MaxHouses:", \
    hillMovesResults.maxHouses)
    print("---------------------------------------------")
    print("Total moves:",int(hillMovesResults.moves))
    print("---------------------------------------------")
    print("Highest score:", hillMovesResults.highestScore)
    print("Lowest score:", hillMovesResults.lowestScore)
    print("Score difference:", hillMovesResults.scoreDifference)
    print("---------------------------------------------")
    print("Total runtime (sec):", hillMovesResults.totalRuntime)
    print("")

    return hillMovesResults

def hillMovesCore(hillMovesResults, oldScore):
    """
    This function picks a random house and random direction to move in, and
    validates whether this is a legit move. It calculates the score and if it is
    higher, the move will not revert. It returns the results of the run.
    """

    # Update round
    hillMovesResults.roundsCounter += 1

    # Only run "rounds" amount of times
    if hillMovesResults.roundsCounter < hillMovesResults.rounds:

        # Extract map and results
        residentialArea = hillMovesResults.highestScoreMap
        numpyGrid = hillMovesResults.numpyGrid

        # Get residentialArea without water (avoiding problems)
        residentialAreaNew = residentialArea[1:len(residentialArea)]

        # Get specific house
        randomHouse = getHouse(residentialArea)
        while randomHouse.type != "maison":
            randomHouse = getHouse(residentialArea)

        # Randomly pick orientation to move in
        orientation = rd.randrange(0,4)      # 0: left, 1: right, 2: up, 3: down

        # Save old begin coordinates (y, x tuple)
        oldCoordinates = (randomHouse.yBegin, randomHouse.xBegin)

        # Remove old position and fix the mess it left behind
        randomHouse.removeFromGridAndMap(numpyGrid)
        redrawGrid(residentialArea, numpyGrid)

        # Update house coordinates 2m in that orientation
        if orientation == 0:      # Go 2m to the left
            yBegin = oldCoordinates[0]
            xBegin = oldCoordinates[1] + 2

        elif orientation == 1:    # Go 2m to the right
            yBegin = oldCoordinates[0]
            xBegin = oldCoordinates[1] - 2

        elif orientation == 2:    # Go 2m up
            yBegin = oldCoordinates[0] + 2
            xBegin = oldCoordinates[1]

        elif orientation == 3:    # Go 2m down
            yBegin = oldCoordinates[0] - 2
            xBegin = oldCoordinates[1]

        # Update new coordinates in self
        changeCoordinates(randomHouse, (yBegin, xBegin))

        # Check restrictions
        if checkAvailableArea(randomHouse, numpyGrid, residentialArea) == True:

            # Move house on numpyGrid
            placeOnHillGrid(randomHouse, numpyGrid)

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

                if currentObject.type == "maison":
                    checkAllFreeArea(currentObject, increase, numpyGrid,
                                    numpyGridOriginal)

                # Then, calculate the new value of each house
                newScore += currentObject.calculateScore()

            # If the score is higher or equal, leave the house on its new spot!
            if newScore >= oldScore:

                print("++ Score:", newScore, "vs.", oldScore, "|| Round:",
                hillMovesResults.roundsCounter)

                # Update scores
                hillMovesResults.highestScore = newScore
                hillMovesResults.highestScoreMap = residentialArea
                hillMovesResults.moves += 1

                # Update score to compare against
                oldScore = newScore

                # Create image of current map
                if hillMovesResults.FFmpegChoice == 1:
                    createImage("hillMoves", residentialArea, hillMovesResults)

                # Run hillMoves again
                hillMovesCore(hillMovesResults, oldScore)

            # Else, score is lower
            else:

                print("   Score:", newScore, "vs.", oldScore, "|| Round:",
                hillMovesResults.roundsCounter)

                # Revert to old coordinates and fix numpyGrid
                revertSingleHouse(randomHouse, oldCoordinates, residentialArea,
                numpyGrid)

                # Run hillMoves again
                hillMovesCore(hillMovesResults, oldScore)

        else:

            # Revert to old coordinates and fix numpyGrid
            revertSingleHouse(randomHouse, oldCoordinates, residentialArea,
            numpyGrid)

            # Run hillMoves again
            hillMovesCore(hillMovesResults, oldScore)

    else:
        return hillMovesResults

def simAnnealing(simAnnealingResults, oldScore):
    """
    This algorithm creates a simulated annealing solution to organize a
    residential area. It loops and searches for solutions until minimum
    temperature has been reached. When minimum has been reached, it keeps the
    solution with the best score found.
    """

    # Set up temperature, minimum temperature, cooling and counter for rounds
    temperature = 20
    minimumTemperature = 1
    cooling = 0.003
    round = 0

    # Loop until minimum temperature is reached
    while temperature >= minimumTemperature:

        # Extract map and results
        residentialArea = simAnnealingResults.currentScoreMap
        numpyGrid = simAnnealingResults.numpyGrid

        # Get residentialArea without water (avoiding problems)
        residentialAreaNew = residentialArea[1:len(residentialArea)]

        # Get specific house
        randomHouse = getHouse(residentialArea)
        while randomHouse.type != "maison":
            randomHouse = getHouse(residentialArea)

        # Randomly pick orientation to move in
        orientation = rd.randrange(0,4)      # 0: left, 1: right, 2: up, 3: down

        # Save old begin coordinates (y, x tuple)
        oldCoordinates = (randomHouse.yBegin, randomHouse.xBegin)

        # Remove old position and fix the mess it left behind
        randomHouse.removeFromGridAndMap(numpyGrid)
        redrawGrid(residentialArea, numpyGrid)

        # Update house coordinates 2m in that orientation
        if orientation == 0:      # Go 2m to the left
            yBegin = oldCoordinates[0]
            xBegin = oldCoordinates[1] + 2

        elif orientation == 1:    # Go 2m to the right
            yBegin = oldCoordinates[0]
            xBegin = oldCoordinates[1] - 2

        elif orientation == 2:    # Go 2m up
            yBegin = oldCoordinates[0] + 2
            xBegin = oldCoordinates[1]

        elif orientation == 3:    # Go 2m down
            yBegin = oldCoordinates[0] - 2
            xBegin = oldCoordinates[1]

        # Update new coordinates in self
        changeCoordinates(randomHouse, (yBegin, xBegin))

        # Check restrictions
        if checkAvailableArea(randomHouse, numpyGrid, residentialArea) == True:

            # Initialize the score of this round
            newScore = 0

            # Move house on numpyGrid
            placeOnHillGrid(randomHouse, numpyGrid)

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

                if currentObject.type == "maison":
                    checkAllFreeArea(currentObject, increase, numpyGrid,
                                    numpyGridOriginal)

                # Then, calculate the new value of each house
                newScore += currentObject.calculateScore()

            # If the score is higher or equal, leave the house on its new spot!
            if newScore >= oldScore:

                print("++ Score:", newScore, "vs.", oldScore, "|| Round:",
                round,"|| Temp:",temperature)

                # Update scores and maps
                simAnnealingResults.currentScore = newScore
                simAnnealingResults.currentScoreMap = residentialArea
                simAnnealingResults.numpyGrid = numpyGrid
                simAnnealingResults.moves += 1

                # Update score to compare against
                oldScore = newScore

                # Create image of current map
                if simAnnealingResults.FFmpegChoice == 1:
                    createImage("simAnnealing", residentialArea,
                    simAnnealingResults)

                # Keep track of best solution found
                if newScore > simAnnealingResults.highestScore:
                    simAnnealingResults.highestScore = newScore
                    simAnnealingResults.highestScoreMap = residentialArea

            # Else, score is lower
            else:

                if acceptProbability(oldScore, newScore, temperature) == True:

                    print("-- Score:", newScore, "vs.", oldScore, "|| Round:",
                    round,"|| Temp:",temperature)

                    # Update scores and maps
                    simAnnealingResults.currentScore = newScore
                    simAnnealingResults.currentScoreMap = residentialArea
                    simAnnealingResults.numpyGrid = numpyGrid
                    simAnnealingResults.moves += 1

                    # Update score to compare against
                    oldScore = newScore

                    # Create image of current map
                    if simAnnealingResults.FFmpegChoice == 1:
                        createImage("simAnnealing", residentialArea,
                        simAnnealingResults)

                else:

                    print("   Score:", newScore, "vs.", oldScore, "|| Round:",
                    round,"|| Temp:",temperature)

                    # Revert to old coordinates and fix numpyGrid
                    revertSingleHouse(randomHouse, oldCoordinates,
                    residentialArea, numpyGrid)

            # Update temperature and round
            temperature *= 1 - cooling
            round += 1

        else:

            # Revert to old coordinates and fix numpyGrid
            revertSingleHouse(randomHouse, oldCoordinates, residentialArea,
            numpyGrid)

    else:

        # Update rounds
        simAnnealingResults.rounds = round

        return simAnnealingResults
