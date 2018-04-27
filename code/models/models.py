"""
models.py

CODERS      Amy van der Gun     10791760
            Bas Katsma          10787690
            Felicia van Gastel  11096187

USAGE       to-do
"""
# %%
from random import randint

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

    # Visualize grid with arrays
    def drawGrid(self):
        """
        grid[0][0]          is linksboven
        grid[Y]grid[X]      coordinate system
        """

        # Create empty grid and initialize fill
        grid = []
        fillNumber = 0

        # Iterate YLength times and add empty array
        for i in range(self.gridYLength):
            row = []
            grid.append(row)

            # Add XLength times a fillNumber per array
            for j in range(self.gridXLength):
                row.append(fillNumber)

        # Random place function
        self.placeOnGrid(grid)

        # Print whole grid
        for element in grid:
            print(element)

        return grid

    # Place on grid function
    def placeOnGrid(self, grid):

        eengezinswoning = 1
        bungalow = 2
        maison = 3

        grid[randint(-1,15)][randint(-1,17)] = eengezinswoning
        grid[randint(-1,15)][randint(-1,17)] = bungalow
        grid[randint(-1,15)][randint(-1,17)] = maison








# # Initialize genericHouse class
# class genericHouse:
#     """
#     Generic House class that contains functions that all the subclasses use
#     """
#
#     def __init__(self):
#         print("genericHouse is made.")
#
#     # Calculates the new price of the property, based on the extra free area
#     def calculateNewValue(self):
#         # Extra vrijstand * base percentage
#         totalIncreasePercentage = self.extraFreeArea * self.valueIncrease
#
#         # Base price + (base price * total percentage)
#         newHouseValue = self.value + (self.value * totalIncreasePercentage)
#
#         return newHouseValue
#
# # Eengezinswoning
# class Eengezinswoning(genericHouse):
#     def __init__(self, gridXLength, gridYLength):
#         self.type = "eengezinswoning"
#         self.houseDimensions = (8, 8)       # (length, depth) tuple
#         self.freeArea = 2      # Vrijstand in meters
#         self.extraFreeArea = 5     # Extra vrijstand in meters
#         self.value = 285000
#         self.valueIncrease = float(0.03)
#         self.positionX = 0
#         self.positionY = 0
#
# # Bungalow
# class Bungalow(genericHouse):
#     def __init__(self, gridXLength, gridYLength):
#         self.type = "bungalow"
#         self.houseDimensions = (10, 7.5)        # (length, depth) tuple
#         self.freeArea = 3      # Vrijstand in meters
#         self.extraFreeArea = 0     # Extra vrijstand in meters
#         self.value = 399000
#         self.valueIncrease = float(0.04)
#         self.positionX = 0
#         self.positionY = 0
#
# # Maison
# class Maison(genericHouse):
#     def __init__(self, gridXLength, gridYLength):
#         self.type = "maison"
#         self.houseDimensions = (11, 10.5)       # (length, depth) tuple
#         self.freeArea = 6      # Vrijstand in meters
#         self.extraFreeArea = 0     # Extra vrijstand in meters
#         self.value = 610000
#         self.valueIncrease = float(0.06)
#         self.positionX = 0
#         self.positionY = 0
