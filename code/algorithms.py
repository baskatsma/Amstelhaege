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

    # Get a random map
    randomMap = initializeRandomMap()

    # Extract map and results
    residentialArea = randomMap[0]
    numpyGrid = randomMap[1]
    currentResult = randomMap[2]

    # Print score
    print("The total score is:", currentResult.highestScore)

    # Update algorithm runtime
    timeEnd = timer()
    runtime = (timeEnd - timeStart)

    # Save current results
    currentResult.fastestRuntime = runtime
    currentResult.highestScoreMap = residentialArea

    # Update randomResults template with the current results
    randomResults.maxHouses = currentResult.maxHouses
    randomResults.totalRuntime += runtime

    # Based on the current results, check for higher/lower scores and update
    randomResults = updateResults(currentResult, randomResults)

    # Print runtime
    print("Total elapsed time (in seconds):",randomResults.totalRuntime)
    print("")

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

# Run hillclimber algorithm
def hillclimberAlgorithm(hillclimberResults, randomResults):

    # Remove old output results
    for png in glob.glob("tmp/*.png"):
        os.remove(png)

    for mp4 in glob.glob("tmp/*.mp4"):
        os.remove(mp4)

    # Measure algorithm time
    timeStart = timer()

    # # Get a random map
    # randomMap = initializeRandomMap()
    #
    # # Extract map and results
    # residentialArea = randomMap[0]
    # numpyGrid = randomMap[1]
    # currentResult = randomMap[2]

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
    print("Rounds:",hillclimberResults.rounds)
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

                print("++ Score:", newScore, "vs.", oldScore, "|| round:",
                hillclimberResults.roundsCounter)

                # Update scores
                #hillclimberResults.highestScore = 0
                hillclimberResults.highestScore = newScore
                #hillclimberResults.highestScoreMap = []
                hillclimberResults.highestScoreMap = residentialArea
                hillclimberResults.swaps += 1

                # Update score to compare against
                oldScore = newScore

                # Run hillclimber again
                hillclimberCore(hillclimberResults, residentialArea,
                                numpyGrid, oldScore)

            # Else, score is lower
            else:

                print("-- Score:", newScore, "vs.", oldScore, "|| round:",
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
