# %% Import classes
import matplotlib.pyplot as plt
import random as rd
from models.models import *
from models.templates import *
from functions import *

def hillclimberAlgorithm(allResults):
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

    # Initialize current and new score
    currentResult = {
                    "totalScore": 0,
                    "runtime": 0,
                    "residentialArea": [],
                    }

    currentScore = 0
    newScore = 0

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
            currentResult["totalScore"] += currentObject.calculateScore()

    results = switchCoordinates(residentialArea, numpyGrid)
    print(results)
    randomHouse1 = results[0]
    randomHouse2 = results[1]

    # print (randomHouse1.uniqueID)
    # print(randomHouse1.type)
    # print (randomHouse2.uniqueID)
    # print(randomHouse2.type)
    # #
    # placeOnGridHILL(randomHouse1, numpyGrid, residentialArea)
    # placeOnGridHILL(randomHouse2, numpyGrid, residentialArea)
    #
    # # After placing all houses, loop over them
    # for object in range(len(residentialArea)):
    #
    #     # Give the current object an easy variable
    #     currentObject = residentialArea[object]
    #
    #     # Calculate score if current item is not water
    #     if currentObject.type != "water":
    #
    #         # Find all extra free area per house
    #         increase = (1 * 2)
    #         numpyGridOriginal = numpyGrid
    #         checkAllFreeArea(currentObject, increase, numpyGrid,
    #                          numpyGridOriginal)
    #
    #         # Then, calculate the new value of the house
    #         newScore += currentObject.calculateScore()
    #
    # print("The new score is:", newScore)
    # # if currentScore > newScore:
    #
    # # Print score
    # print("The total score is:", currentResult["totalScore"])
    #
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

    # Select random house
    randomHouse1 = residentialArea[rd.randrange(len(residentialArea))]
    randomHouse2 = residentialArea[rd.randrange(len(residentialArea))]


    # Retry if selected house is 'water', or when both houses are the same
    while randomHouse1.uniqueID == 200 or randomHouse2.uniqueID == 200 or \
        randomHouse1.uniqueID == randomHouse2.uniqueID:

        print("HAPPY LIFE")

        # Select random house
        randomHouse1 = residentialArea[rd.randrange(len(residentialArea))]
        randomHouse2 = residentialArea[rd.randrange(len(residentialArea))]
        break

    # Save old and new coordinates
    oldCoordinates1 = (randomHouse1.yBegin, randomHouse1.xBegin)
    oldCoordinates2 = (randomHouse2.yBegin, randomHouse2.xBegin)
    newCoordinates1 = oldCoordinates2
    newCoordinates2 = oldCoordinates1

    # Remove houses from map and numpyGrid
    randomHouse1.removeFromGridAndMap(numpyGrid)
    randomHouse2.removeFromGridAndMap(numpyGrid)

    # Update coordinates
    updateCoordinates(randomHouse1, newCoordinates1)
    updateCoordinates(randomHouse2, newCoordinates2)
    
    return [randomHouse1, randomHouse2]


def placeOnGridHILL(currentObject, numpyGrid, residentialArea):

    # Get random coordinates and update in self
    # getCoordinates(currentObject)

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
            print("huis overlap")
            # results2 = switchCoordinates(residentialArea)
            # placeOnGridHILL(results2[0], numpyGrid, residentialArea)
            # placeOnGridHILL(results2[1], numpyGrid, residentialArea)

    # Start over, because the house is overlining the border
    else:
        print("border problemsssss xxx amy")
        # results3 = switchCoordinates(residentialArea)
        #
        # placeOnGridHILL(results3[0], numpyGrid, residentialArea)
        # placeOnGridHILL(results3[1], numpyGrid, residentialArea)
