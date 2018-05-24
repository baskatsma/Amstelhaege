import random as rd
import math as mt
import numpy as np

class Water(object):
    """
    Contains all water properties and functions
    """

    def __init__(self, type, freeArea, extraFreeArea, gridXLength, gridYLength,
                xBegin, xEnd, yBegin, yEnd, uniqueID):
        self.totalSquareArea = 0.2 * int(gridXLength) * int(gridYLength)
        self.type = type
        self.freeArea = freeArea
        self.extraFreeArea = extraFreeArea
        self.gridXLength = gridXLength
        self.gridYLength = gridYLength
        self.objectDimensions = (int(self.totalSquareArea/296), 296)
        self.xBegin = xBegin
        self.xEnd = xEnd
        self.yBegin = yBegin
        self.yEnd = yEnd
        self.uniqueID = uniqueID

# Define House class
class House(object):
    """
    Contains all house properties and functions
    """

    def __init__(self, type, objectDimensions, freeArea, extraFreeArea, value,
    valueIncrease, xBegin, xEnd, yBegin, yEnd, gridXLength, gridYLength, uniqueID):
        self.type = type
        self.objectDimensions = (int(objectDimensions[0] * 2),
                                int(objectDimensions[1] * 2))
        self.freeArea = (freeArea * 2)
        self.extraFreeArea = (extraFreeArea * 2)
        self.value = value
        self.valueIncrease = valueIncrease
        self.xBegin = xBegin
        self.xEnd = xEnd
        self.yBegin = yBegin
        self.yEnd = yEnd
        self.gridXLength = gridXLength
        self.gridYLength = gridYLength
        self.uniqueID = uniqueID

    def removeFromGridAndMap(self, numpyGrid):

        # Define coordinate variables
        yBegin = self.yBegin
        yEnd = self.yEnd
        xBegin = self.xBegin
        xEnd = self.xEnd
        freeArea = self.freeArea

        fAYBegin = yBegin - freeArea
        fAYEnd = yEnd + freeArea
        fAXBegin = xBegin - freeArea
        fAXEnd = xEnd + freeArea

        # Delete selected house + free area from numpyGrid
        numpyGrid[fAYBegin:fAYEnd,fAXBegin:fAXEnd] = 0

        # Position house in (0, 0)
        self.xBegin = 0
        self.xEnd = 0
        self.yBegin = 0
        self.yEnd = 0

    def checkBorders(self):

        # Check for grid border problems
        if \
        (self.yEnd + self.freeArea + self.extraFreeArea) > self.gridYLength or \
        (self.xEnd + self.freeArea + self.extraFreeArea) > self.gridXLength or \
        (self.xBegin - self.freeArea - self.extraFreeArea) <= 0 or \
        (self.yBegin - self.freeArea - self.extraFreeArea) <= 0:
            return False

        # No grid border problems, continuing
        else:
            return True

    # Calculate and return score per house
    def calculateScore(self):

        scoreHouse = self.value + (self.value * \
                    (self.valueIncrease * self.extraFreeArea))

        return int(scoreHouse)

# Define GridInformation class
class GridInformation(object):
    """
    Class that contains all information about the grid
    """

    def __init__(self, gridXLength, gridYLength, maxHouses):
        self.gridXLength = gridXLength
        self.gridYLength = gridYLength
        self.maxHouses = maxHouses
        self.fractionEengezinswoningen = float(0.60)
        self.fractionBungalows = float(0.25)
        self.fractionMaisons = float(0.15)
        self.totalAmountEengezinswoningen = int(self.maxHouses *
        self.fractionEengezinswoningen)
        self.totalAmountBungalows = int(self.maxHouses * self.fractionBungalows)
        self.totalAmountMaisons = int(self.maxHouses * self.fractionMaisons)

# Define Results class
class Results(object):
    """
    Class that contains all results
    """

    def __init__(self, algorithm, maxHouses, rounds, roundsCounter, swaps, moves,
    allScores, currentScore, currentScoreMap, highestScore, highestScoreMap,
    numpyGrid, lowestScore, scoreDifference, fastestRuntime, slowestRuntime,
    totalRuntime):
        self.algorithm = algorithm
        self.maxHouses = maxHouses
        self.rounds = rounds
        self.roundsCounter = roundsCounter
        self.swaps = swaps
        self.moves = moves
        self.allScores = allScores
        self.currentScore = currentScore
        self.currentScoreMap = currentScoreMap
        self.highestScore = highestScore
        self.highestScoreMap = highestScoreMap
        self.numpyGrid = numpyGrid
        self.lowestScore = lowestScore
        self.scoreDifference = highestScore - lowestScore
        self.fastestRuntime = fastestRuntime
        self.slowestRuntime = slowestRuntime
        self.totalRuntime = totalRuntime
