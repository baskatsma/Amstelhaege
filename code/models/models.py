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

# Define House class
class House(object):
    """
    Contains all house properties and functions
    """

    def __init__(self, type, houseDimensions, freeArea, extraFreeArea, value,
    valueIncrease, positionX, positionY, gridXLength, gridYLength, uniqueID):
        self.type = type
        self.houseDimensions = houseDimensions
        self.freeArea = freeArea
        self.extraFreeArea = extraFreeArea
        self.value = value
        self.valueIncrease = valueIncrease
        self.positionX = positionX
        self.positionY = positionY
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
        self.positionY = rd.randrange(self.gridYLength - 5)
        self.positionX = rd.randrange(self.gridXLength - 5)
        beginCoordinates = (self.positionY, self.positionX)

        return beginCoordinates

    def drawOnGrid(self, buildingSite, currentHouse):

        # Define number that numpy will draw
        drawNumber = currentHouse.uniqueID
        # if currentHouse.type == "eengezinswoning":
        #     drawNumber = 2
        # elif currentHouse.type == "bungalow":
        #     drawNumber = 3
        # elif currentHouse.type == "maison":
        #     drawNumber = 4

        # Get begin coordinates (y, x tuple) randomly
        beginCoordinates = self.getBeginCoordinates()

        # Extract house dimension values
        houseYLength = self.houseDimensions[1]
        houseXLength = self.houseDimensions[0]

        # Define end coordinates (y, x tuple)
        endCoordinates = (beginCoordinates[0] + houseYLength, beginCoordinates[1]
        + houseXLength)

        # Define new coordinates
        yCoordinateBegin = beginCoordinates[0]
        yCoordinateEnd = endCoordinates[0]
        xCoordinateBegin = beginCoordinates[1]
        xCoordinateEnd = endCoordinates[1]

        # Print tests
        print("This is a",currentHouse.type,"with uniqueID:",currentHouse.uniqueID)
        # print("beginCoordinates(Y, X): ",beginCoordinates)
        # print("endCoordinates(Y, X): ",endCoordinates)
        # print("YLength is: ",houseYLength, end="")
        # print("  ||  XLength is: ",houseXLength)

        # Check for overlap
        if self.noOverlap(yCoordinateBegin, yCoordinateEnd, xCoordinateBegin,
        xCoordinateEnd, buildingSite) == True:

            # Field is clear, update grid
            buildingSite[yCoordinateBegin:yCoordinateEnd,xCoordinateBegin:xCoordinateEnd] = drawNumber

        # Start over with drawOnGrid for this specific house
        else:
            print("Fetching new coordinates, because of overlap")
            self.drawOnGrid(buildingSite, currentHouse)

    def noOverlap(self, yCoordinateBegin, yCoordinateEnd, xCoordinateBegin,
    xCoordinateEnd, buildingSite):

        # Print statements
        # print("Checking buildingSite[Y,X]   [",yCoordinateBegin,"tot",
        # yCoordinateEnd,end="")
        # print(" ,",xCoordinateBegin,"tot",xCoordinateEnd,"]")
        # print("")

        # Check house dimension area starting at the begin coordinates
        if np.any(buildingSite[yCoordinateBegin:yCoordinateEnd,
        xCoordinateBegin:xCoordinateEnd] != 0):
            return False

        else:
            return True

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
