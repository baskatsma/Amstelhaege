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

# Define House class
class House(object):
    """
    Contains all house properties and functions
    """

    def __init__(self, type, houseDimensions, freeArea, extraFreeArea, value,
    valueIncrease, xBegin, xEnd, yBegin, yEnd, gridXLength, gridYLength, uniqueID):
        self.type = type
        self.houseDimensions = houseDimensions
        self.freeArea = freeArea
        self.extraFreeArea = extraFreeArea
        self.value = value
        self.valueIncrease = valueIncrease
        self.xBegin = xBegin
        self.xEnd = xEnd
        self.yBegin = yBegin
        self.yEnd = yEnd
        self.gridXLength = gridXLength
        self.gridYLength = gridYLength
        self.uniqueID = uniqueID

    # Calculates the new price of the property, based on the extra free area
    def calculateNewValue(self):

        # Extra vrijstand * base percentage
        totalIncreasePercentage = self.extraFreeArea * self.valueIncrease

        # Base price + (base price * total percentage)
        newHouseValue = self.value + (self.value * totalIncreasePercentage)

        return newHouseValue

    def getBeginCoordinates(self):

        # To-do: Remove -5 and correctly work with borders
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

        # Print tests
        print("This is a",self.type,"with uniqueID:",self.uniqueID)
        # print("beginCoordinates(Y, X): ",beginCoordinates)
        # print("endCoordinates(Y, X): ",endCoordinates)
        # print("YLength is: ",houseYLength, end="")
        # print("  ||  XLength is: ",houseXLength)

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

        # Print statements
        # print("Checking numpyGrid[Y,X]   [",self.yBegin,"tot",
        # self.yEnd,end="")
        # print(" ,",self.xBegin,"tot",self.xEnd,"]")
        # print("")

        # Check house dimension area starting at the begin coordinates
        if np.any(numpyGrid[self.yBegin:self.yEnd,self.xBegin:self.xEnd] != 0):
            return False

        else:
            return True

    def calculateScore(self):

        scoreHouse = self.value + self.valueIncrease * self.extraFreeArea

        return scoreHouse

# Define Grid class
class Grid(object):
    """
    Grid that contains all houses
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
