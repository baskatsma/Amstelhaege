"""
models.py

CODERS      Amy van der Gun     10791760
            Bas Katsma          10787690
            Felicia van Gastel  11096187

USAGE       to-do
"""
# %%
import random as rd
import numpy as np
import matplotlib.pyplot as plt

class Water(object):
    """
    Contains all water properties and functions
    """

    def __init__(self, totalSquareArea, amountOfWater, waterDimensions):
        self.totalSquareArea = 0.2 * gridXLength * gridYLength
        self.amountOfWater = rd.randint(1,4)
        self.waterDimensions = (int(waterDimensions[0]), int(waterDimensions[1]))





# Define House class
class House(object):
    """
    Contains all house properties and functions
    """

    def __init__(self, type, houseDimensions, freeArea, extraFreeArea, value,
    valueIncrease, xBegin, xEnd, yBegin, yEnd, gridXLength, gridYLength, uniqueID):
        self.type = type
        self.houseDimensions = (int(houseDimensions[0] * 2),
                                int(houseDimensions[1] * 2))
        self.freeArea = freeArea * 2
        self.extraFreeArea = extraFreeArea * 2
        self.value = value
        self.valueIncrease = valueIncrease
        self.xBegin = xBegin
        self.xEnd = xEnd
        self.yBegin = yBegin
        self.yEnd = yEnd
        self.gridXLength = gridXLength
        self.gridYLength = gridYLength
        self.uniqueID = uniqueID

    def getBeginCoordinates(self):

        # Set new begin coordinates and save them in self
        self.yBegin = rd.randrange(self.gridYLength)
        self.xBegin = rd.randrange(self.gridXLength)
        beginCoordinates = (self.yBegin, self.xBegin)

        return beginCoordinates

    def drawOnGrid(self, numpyGrid):

        # Use uniqueID number to visualize
        drawNumber = self.uniqueID

        # Extract house dimension values
        houseYLength = self.houseDimensions[1]
        houseXLength = self.houseDimensions[0]

        # Get begin coordinates (y, x tuple) randomly
        beginCoordinates = self.getBeginCoordinates()

        # Define end coordinates (y, x tuple)
        endCoordinates = (beginCoordinates[0] + houseYLength,
                          beginCoordinates[1] + houseXLength)

        # Update coordinates
        self.yBegin = beginCoordinates[0]
        self.yEnd = endCoordinates[0]
        self.xBegin = beginCoordinates[1]
        self.xEnd = endCoordinates[1]

        # Check whether houses are in the grid
        if self.yEnd > self.gridYLength or self.xEnd > self.gridXLength:
            self.drawOnGrid(numpyGrid)

        else:

            # Check for overlap
            if self.checkOverlap(self.yBegin, self.yEnd, self.xBegin,
                                 self.xEnd, numpyGrid) == True:

                # Field is clear, update grid
                numpyGrid[self.yBegin:self.yEnd,
                          self.xBegin:self.xEnd] = drawNumber

            # Start over with drawOnGrid for this specific house
            else:
                print("Fetching new coordinates, because of overlap")
                self.drawOnGrid(numpyGrid)

    def checkOverlap(self, yBegin, yEnd, xBegin, xEnd, numpyGrid):

        # Check house dimension area starting at the begin coordinates
        if np.any(numpyGrid[self.yBegin:self.yEnd,self.xBegin:self.xEnd] != 0):
            return False

        else:
            return True

    # Calculate and return score per house
    def calculateScore(self):

        scoreHouse = self.value + self.value * (self.valueIncrease * self.extraFreeArea)

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
