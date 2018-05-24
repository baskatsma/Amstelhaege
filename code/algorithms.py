import glob
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
    This algorithm creates a random solution to organize a residental area.
    """

    # Update results sheet
    randomResults.algorithm = "random"

    # Remove old output results
    for png in glob.glob("tmp/*.png"):
        os.remove(png)

    for mp4 in glob.glob("tmp/*.mp4"):
        os.remove(mp4)

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

        # Print high/low score & runtime
        print("")
        print("Rounds:", randomResults.rounds, "|| MaxHouses:", \
        randomResults.maxHouses)
        print("---------------------------------------------")
        print("Highest score:", randomResults.highestScore)
        print("Lowest score:", randomResults.lowestScore)
        print("Average score:", randomResults.averageScore)
        print("---------------------------------------------")
        print("Total runtime (sec):", randomResults.totalRuntime)
        print("")

    return randomResults

# Run hillSwaps algorithm
def hillSwapsAlgorithm(hillSwapsResults, randomResults):
    """
    This algorithm creates an hillclimber solution to organize a
    residental area.
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
    for png in glob.glob("tmp/*.png"):
        os.remove(png)

    for mp4 in glob.glob("tmp/*.mp4"):
        os.remove(mp4)

    # Extract result
    oldScore = randomResults.highestScore

    # Do hillSwaps "rounds" amount of times
    hillSwapsCore(hillSwapsResults, oldScore)

    # Update algorithm runtime
    timeEnd = timer()
    runtime = (timeEnd - timeStart)
    hillSwapsResults.totalRuntime += runtime

    # Print high/low score & runtime
    print("")
    print("Rounds:", hillSwapsResults.rounds, "|| MaxHouses:", \
    hillSwapsResults.maxHouses)
    print("---------------------------------------------")
    print("Total swaps:",int(hillSwapsResults.swaps))
    print("---------------------------------------------")
    print("Highest score:", hillSwapsResults.highestScore)
    print("Lowest score:", hillSwapsResults.lowestScore)
    print("Average score:", hillSwapsResults.averageScore)
    print("---------------------------------------------")
    print("Total runtime (sec):", hillSwapsResults.totalRuntime)
    print("")

    return hillSwapsResults

def hillSwapsCore(hillSwapsResults, oldScore):
    """
    THIS FUNCTION GEEN IDEE XXX
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

                # Run hillSwaps again
                hillSwapsCore(hillSwapsResults, oldScore)

            # Else, score is lower
            else:

                print("-- Score:", newScore, "vs.", oldScore, "|| Round:",
                hillSwapsResults.roundsCounter)

                # Revert to old coordinates and fix numpyGrid
                revertSituation(randomHouse1, randomHouse2, oldCoordinates1,
                                oldCoordinates2, numpyGrid, residentialArea)

                # Re-calculate extra free area for this old situation
                recalculateAllExtraFreeArea(residentialArea, numpyGrid)

                # Run hillSwaps again
                hillSwapsCore(hillSwapsResults, oldScore)

        else:

            # Revert to old coordinates and fix numpyGrid
            revertSituation(randomHouse1, randomHouse2, oldCoordinates1,
                            oldCoordinates2, numpyGrid, residentialArea)

            # Re-calculate extra free area for this old situation
            recalculateAllExtraFreeArea(residentialArea, numpyGrid)

            # Run hillSwaps again
            hillSwapsCore(hillSwapsResults, oldScore)

    else:

        return hillSwapsResults

def hillMovesAlgorithm(hillMovesTemplate, choice):
    """
    This algorithm creates an heuristic hillclimber solution to organize a
    residental area.
    """

    # Measure algorithm time
    timeStart = timer()

    # Update template
    hillMovesTemplate.algorithm = "hillMoves"

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

            # Place eengezinswoningen
            if currentObject.type == "eengezinswoning":

                dimensions = (currentObject.objectDimensions[0]
                            + currentObject.freeArea)
                print(currentObject.objectDimensions[0] + currentObject.freeArea * 2)
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
            hillMovesTemplate.highestScore += currentObject.calculateScore()

    # Save current results
    hillMovesTemplate.lowestScore = hillMovesTemplate.highestScore
    hillMovesTemplate.maxHouses = maxHouses
    hillMovesTemplate.highestScoreMap = residentialArea
    hillMovesTemplate.numpyGrid = numpyGrid

    # Define score to compare against
    oldScore = hillMovesTemplate.highestScore

    if choice == "hillMoves":
        hillMovesMove(hillMovesTemplate, oldScore)

    elif choice == "simAnnealing":
        simAnnealing(hillMovesTemplate, oldScore)

    # Update runtime
    timeEnd = timer()
    runtime = (timeEnd - timeStart)
    hillMovesTemplate.totalRuntime = runtime

    # Print high/low score & runtime
    print("")
    print("Rounds:", hillMovesTemplate.rounds, "|| MaxHouses:", \
    hillMovesTemplate.maxHouses)
    print("---------------------------------------------")
    print("Total moves:",int(hillMovesTemplate.moves))
    print("---------------------------------------------")
    print("Highest score:", hillMovesTemplate.highestScore)
    print("Lowest score:", hillMovesTemplate.lowestScore)
    print("Average score:", hillMovesTemplate.averageScore)
    print("---------------------------------------------")
    print("Total runtime (sec):", hillMovesTemplate.totalRuntime)
    print("")

    return hillMovesTemplate

def hillMovesMove(hillMovesTemplate, oldScore):
    """
    THIS FUNCTION GEEEEEEN IDEEEEEEE
    """

    # Update round
    hillMovesTemplate.roundsCounter += 1

    # Only run "rounds" amount of times
    if hillMovesTemplate.roundsCounter < hillMovesTemplate.rounds:

        # Extract map and results
        residentialArea = hillMovesTemplate.highestScoreMap
        numpyGrid = hillMovesTemplate.numpyGrid

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
        fixIncorrectVisualizations(residentialArea, numpyGrid)

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
        updateCoordinates(randomHouse, (yBegin, xBegin))

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
                hillMovesTemplate.roundsCounter)

                # Update scores
                hillMovesTemplate.highestScore = newScore
                hillMovesTemplate.highestScoreMap = residentialArea
                hillMovesTemplate.moves += 1

                # Update score to compare against
                oldScore = newScore

                # Run hillMoves again
                hillMovesMove(hillMovesTemplate, oldScore)

            # Else, score is lower
            else:

                print("-- Score:", newScore, "vs.", oldScore, "|| Round:",
                hillMovesTemplate.roundsCounter)

                # Revert to old coordinates and fix numpyGrid
                # Remove houses from numpyGrid and map
                randomHouse.removeFromGridAndMap(numpyGrid)

                # Revert to old coordinates
                updateCoordinates(randomHouse, oldCoordinates)

                # Clean-up some bugs and plot old location back
                fixIncorrectVisualizations(residentialArea, numpyGrid)

                # Re-calculate extra free area for this old situation
                recalculateAllExtraFreeArea(residentialArea, numpyGrid)

                # Run hillSwaps again
                hillMovesMove(hillMovesTemplate, oldScore)

        else:

            # Revert to old coordinates and fix numpyGrid
            # Remove houses from numpyGrid and map
            randomHouse.removeFromGridAndMap(numpyGrid)

            # Revert to old coordinates
            updateCoordinates(randomHouse, oldCoordinates)

            # Clean-up some bugs and plot old location back
            fixIncorrectVisualizations(residentialArea, numpyGrid)

            # Re-calculate extra free area for this old situation
            recalculateAllExtraFreeArea(residentialArea, numpyGrid)

            # Run hillSwaps again
            hillMovesMove(hillMovesTemplate, oldScore)

    else:
        return hillMovesTemplate

def simAnnealing(hillMovesTemplate, oldScore):
    """
    This algorithm creates a simulated annealing solution to organize a
    residental area. It loops and searches for solutions until minimum
    temperature has been reached. When minimum has been reached, it keeps the
    solution with the best score found.
    """

    # Set up temperature, minimum temperature, cooling and counter for rounds
    temperature = 10
    minimumTemperature = 1
    cooling = 0.003
    round = 0

    # Loop until minimum temperature is reached
    while temperature >= minimumTemperature:

        # Extract map and results
        residentialArea = hillMovesTemplate.highestScoreMap
        numpyGrid = hillMovesTemplate.numpyGrid

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
        fixIncorrectVisualizations(residentialArea, numpyGrid)

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
        updateCoordinates(randomHouse, (yBegin, xBegin))

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

                # Update scores
                hillMovesTemplate.currentScore = newScore
                hillMovesTemplate.moves += 1

                # Update score to compare against
                oldScore = newScore

                # Keep track of best solution found
                if newScore > hillMovesTemplate.highestScore:
                    hillMovesTemplate.highestScore = newScore
                    hillMovesTemplate.highestScoreMap = residentialArea
                    hillMovesTemplate.numpyGrid = numpyGrid
                    print ("NEW BEST SCORE =", hillMovesTemplate.highestScore)

            # Else, score is lower
            else:

                if acceptProbability(oldScore, newScore, temperature) == True:

                    print("-- Score:", newScore, "vs.", oldScore, "|| Round:",
                    round,"|| Temp:",temperature)

                    # Update scores
                    hillMovesTemplate.currentScore = newScore
                    hillMovesTemplate.swaps += 1

                    # Update score to compare against
                    oldScore = newScore

                else:

                    print("-- Score:", newScore, "vs.", oldScore, "|| Round:",
                    round,"|| Temp:",temperature)

                    # Revert to old coordinates and fix numpyGrid
                    # Remove houses from numpyGrid and map
                    randomHouse.removeFromGridAndMap(numpyGrid)

                    # Revert to old coordinates
                    updateCoordinates(randomHouse, oldCoordinates)

                    # Clean-up some bugs and plot old location back
                    fixIncorrectVisualizations(residentialArea, numpyGrid)

                    # Re-calculate extra free area for this old situation
                    recalculateAllExtraFreeArea(residentialArea, numpyGrid)

            # Temperature = temperature * cooling factor
            temperature *= 1 - cooling
            round += 1

        else:

            # Revert to old coordinates and fix numpyGrid
            # Remove houses from numpyGrid and map
            randomHouse.removeFromGridAndMap(numpyGrid)

            # Revert to old coordinates
            updateCoordinates(randomHouse, oldCoordinates)

            # Clean-up some bugs and plot old location back
            fixIncorrectVisualizations(residentialArea, numpyGrid)

            # Re-calculate extra free area for this old situation
            recalculateAllExtraFreeArea(residentialArea, numpyGrid)

    else:
        return hillMovesTemplate

def acceptProbability(oldScore, newScore, temperature):
    """
    Computes acceptance probability that will be used by simulated annealing.
    """

    # Get a random float number between 0 and 1
    random0to1 = rd.uniform(0,1)

    # Compute difference between old score and new score
    delta = (newScore - oldScore) / 100000

    # Calculate the acceptance probability
    acceptanceProb = math.exp(delta / temperature)

    print(random0to1)
    print(acceptanceProb)

    # If acceptance probability is higher than random number, accept lower score
    if acceptanceProb >= random0to1:
        return True

    # If not, do not accept lower score
    else:
        return False

"""
Temp. variabelen initializeren +++++++
We loopen net zo lang totdat de minimum temperatuur is bereikt +++++++

    We pakken een random maison +++++++
    We pakken een random richting (0 - 3) +++++++
    Moven we dit maison in die richting +++++++
    Checks uitvoeren of dit mogelijk is +++++++
        Ja: score berekenen +++++++
            Als de newScore hoger of gelijk is dan de oldScore: accepteren +++++++
            Als de newScore lager is dan de oldScore: acceptProbability() +++++++
                if aP returns True: +++++++
                    plaatsen +++++++
                else +++++++
                    terugplaatsen +++++++
                Temperatuur updaten +++++++
        Nee: terugplaatsen +++++++
"""
