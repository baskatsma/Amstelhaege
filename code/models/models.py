"""
models.py

CODERS      Amy van der Gun     10791760
            Bas Katsma          10787690
            Felicia van Gastel  11096187

USAGE       to-do
"""
# %%
import random as rd
import math as mt
import numpy as np
import matplotlib.pyplot as plt

class Water(object):
    """
    Contains all water properties and functions
    """

    def __init__(self, type, freeArea, gridXLength, gridYLength, xBegin, xEnd, yBegin, yEnd, uniqueID):
        self.totalSquareArea = 0.2 * int(gridXLength) * int(gridYLength)
        self.type = type
        self.freeArea = freeArea
        self.gridXLength = gridXLength
        self.gridYLength = gridYLength
        self.waterDimensions = (int(mt.sqrt(self.totalSquareArea)),
                                int(mt.sqrt(self.totalSquareArea)))
        self.xBegin = xBegin
        self.xEnd = xEnd
        self.yBegin = yBegin
        self.yEnd = yEnd
        self.uniqueID = uniqueID

    def drawOnGrid(self, numpyGrid):

        # Use uniqueID number to visualize
        drawNumber = self.uniqueID

        # # Terminal testing purposes
        # if self.type == "eengezinswoning":
        #     self.freeArea = 1
        #     drawNumber = 2
        #
        # elif self.type == "bungalow":
        #     self.freeArea = 1
        #     drawNumber = 3
        #
        # elif self.type == "maison":
        #     self.freeArea = 2
        #     drawNumber = 4

        # elif self.type == "water":
        #     self.freeArea = 0
        #     drawNumber = 7

        # Extract water dimension values
        houseYLength = self.waterDimensions[0]
        houseXLength = self.waterDimensions[1]

        # Begin coordinates (y, x tuple)
        beginCoordinates = (0, 0)

        # Define end coordinates (y, x tuple)
        endCoordinates = (beginCoordinates[0] + houseYLength,
                          beginCoordinates[1] + houseXLength)

        # Update coordinates
        self.yBegin = beginCoordinates[0]
        self.yEnd = endCoordinates[0]
        self.xBegin = beginCoordinates[1]
        self.xEnd = endCoordinates[1]

        # Check for house and free area overlap
        if self.checkHouseOverlap(self.yBegin,
                self.yEnd,
                self.xBegin,
                self.xEnd, numpyGrid) == True:

            # Field is clear, update grid
            numpyGrid[self.yBegin:self.yEnd,
                      self.xBegin:self.xEnd] = drawNumber

        # Start over with drawOnGrid for this specific house
        else:
            #print("Fetching new coordinates, because of any overlap")
            self.drawOnGrid(numpyGrid)

    def checkHouseOverlap(self, newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid):

        # Check house dimension area starting at the begin coordinates
        if np.any(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] != 0):
            return False

        else:
            return True

    def checkFreeAreaOverlap(self, newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid):

        # We willen dat het vrijstands gebied OF helemaal 0 is, OF helemaal 1 \
        # of een mix van beiden. IIG geen uniqueID of 2, 3, 4, 5 etc.
        if np.all(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] <= 1):
            return True

        else:
            #print("There's more than 0 or 1")
            return False

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
        # self.houseDimensions = (houseDimensions[0], houseDimensions[1])
        # self.freeArea = freeArea
        # self.extraFreeArea = extraFreeArea
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

        # # Terminal testing purposes
        # if self.type == "eengezinswoning":
        #     self.freeArea = 1
        #     drawNumber = 2
        #
        # elif self.type == "bungalow":
        #     self.freeArea = 1
        #     drawNumber = 3
        #
        # elif self.type == "maison":
        #     self.freeArea = 2
        #     drawNumber = 4

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

        # Check for grid border problems
        if self.yEnd + self.freeArea > self.gridYLength or \
        self.xEnd + self.freeArea > self.gridXLength or \
        self.xBegin - self.freeArea < 0 or \
        self.yBegin - self.freeArea < 0:
            self.drawOnGrid(numpyGrid)

        # No grid border problems, continuing
        else:

            # Check for house and free area overlap
            if self.checkHouseOverlap(self.yBegin,
                    self.yEnd,
                    self.xBegin,
                    self.xEnd, numpyGrid) == True and \
            self.checkFreeAreaOverlap(self.yBegin,
                    self.yEnd,
                    (self.xBegin - self.freeArea),
                    self.xBegin, numpyGrid) == True and \
            self.checkFreeAreaOverlap(self.yBegin,
                    self.yEnd,
                    self.xEnd,
                    (self.xEnd + self.freeArea), numpyGrid) == True and \
            self.checkFreeAreaOverlap((self.yBegin - self.freeArea),
                    self.yBegin,
                    self.xBegin,
                    self.xEnd, numpyGrid) == True and \
            self.checkFreeAreaOverlap(self.yEnd,
                    (self.yEnd + self.freeArea),
                    self.xBegin,
                    self.xEnd, numpyGrid) == True:

                # Field is clear, update grid
                numpyGrid[self.yBegin:self.yEnd,
                          self.xBegin:self.xEnd] = drawNumber

                numpyGrid[self.yBegin:self.yEnd,
                        self.xBegin - self.freeArea:self.xBegin] = 1

                numpyGrid[self.yBegin:self.yEnd,
                        self.xEnd:self.xEnd + self.freeArea] = 1

                numpyGrid[self.yBegin - self.freeArea:self.yBegin,
                        self.xBegin:self.xEnd] = 1

                numpyGrid[self.yEnd:self.yEnd + self.freeArea,
                        self.xBegin:self.xEnd] = 1

            # Start over with drawOnGrid for this specific house
            else:
                print("Fetching new coordinates, because of any overlap")
                self.drawOnGrid(numpyGrid)

    def checkHouseOverlap(self, newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid):

        # Check house dimension area starting at the begin coordinates
        if np.any(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] != 0):
            return False

        else:
            return True

    def checkFreeAreaOverlap(self, newYBegin, newYEnd, newXBegin, newXEnd, numpyGrid):

        # We willen dat het vrijstands gebied OF helemaal 0 is, OF helemaal 1 \
        # of een mix van beiden. IIG geen uniqueID of 2, 3, 4, 5 etc.
        if np.all(numpyGrid[newYBegin:newYEnd,newXBegin:newXEnd] <= 1):
            return True

        else:
            print("There's more than 0 or 1")
            return False

    # Calculate and return score per house
    def calculateScore(self):

        scoreHouse = self.value + self.value * \
                    (self.valueIncrease * self.extraFreeArea)

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
