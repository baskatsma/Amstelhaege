"""
models.py

CODERS      Amy van der Gun     10791760
            Bas Katsma          10787690
            Felicia van Gastel  11096187

USAGE       to-do
"""
# %%
import random as rd

# Define House class
class House(object):
    """
    Contains all house properties and functions
    """

    def __init__(self, type, houseDimensions, freeArea, extraFreeArea, value, valueIncrease, positionX, positionY, gridXLength, gridYLength, uniqueID):
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

    def drawOnGrid(self, buildingSite, drawNumber):

        # Get begin coordinates randomly
        self.positionY = rd.randrange(self.gridYLength - 5)
        self.positionX = rd.randrange(self.gridXLength - 5)
        beginCoordinates = (self.positionY, self.positionX)

        # Extract house dimension values
        houseXLength = self.houseDimensions[0]
        houseYLength = self.houseDimensions[1]

        # Calculate end coordinates
        endCoordinates = (beginCoordinates[0] + houseYLength, beginCoordinates[1] + houseXLength)

        # Define new coordinates
        yCoordinateBegin = beginCoordinates[0]
        yCoordinateEnd = endCoordinates[0]
        xCoordinateBegin = beginCoordinates[1]
        xCoordinateEnd = endCoordinates[1]

        # Print tests
        print("beginCoordinates: ",beginCoordinates)
        print("endCoordinates: ",endCoordinates)
        print("YLength is: ",houseYLength, end="")
        print("  ||  XLength is: ",houseXLength)
        print("")

        # Update grid
        buildingSite[yCoordinateBegin:yCoordinateEnd,xCoordinateBegin:xCoordinateEnd] = drawNumber


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
        self.totalAmountEengezinswoningen = int(self.maxHouses * self.fractionEengezinswoningen)
        self.totalAmountBungalows = int(self.maxHouses * self.fractionBungalows)
        self.totalAmountMaisons = int(self.maxHouses * self.fractionMaisons)
