"""
models.py

CODERS      Amy van der Gun     10791760
            Bas Katsma          10787690
            Felicia van Gastel  1

USAGE       to-do
"""

# %% Initialize genericHouse class
class genericHouse:
    """
    Generic House class that contains functions that all the subclasses use
    """

    def __init__(self):
        print("genericHouse is made.")

    # To do: add positional functions, get value, etc. etc. etc.

    # Calculates the new price of the property, based on the extra free area
    def calculateNewValue(self):
        # Extra vrijstand * base percentage
        totalIncreasePercentage = self.extraFreeArea * self.valueIncrease

        # Base price + (base price * total percentage)
        newHouseValue = self.value + (self.value * totalIncreasePercentage)
        return newHouseValue


# %% Eengezinswoning
class Eengezinswoning(genericHouse):
    def __init__(self, gridXLength, gridYLength):
        self.type = "eengezinswoning"
        self.houseDimensions = (8, 8)       # (length, depth) tuple
        self.freeArea = 2      # Vrijstand in meters
        self.extraFreeArea = 5     # Extra vrijstand in meters
        self.value = 285000
        self.valueIncrease = float(0.03)

# %% Bungalow
class Bungalow(genericHouse):
    def __init__(self, gridXLength, gridYLength):
        self.type = "bungalow"
        self.houseDimensions = (10, 7.5)        # (length, depth) tuple
        self.freeArea = 3      # Vrijstand in meters
        self.extraFreeArea = 0     # Extra vrijstand in meters
        self.value = 399000
        self.valueIncrease = float(0.04)

# %% Maison
class Maison(genericHouse):
    def __init__(self, gridXLength, gridYLength):
        self.type = "maison"
        self.houseDimensions = (11, 10.5)       # (length, depth) tuple
        self.freeArea = 6      # Vrijstand in meters
        self.extraFreeArea = 0     # Extra vrijstand in meters
        self.value = 610000
        self.valueIncrease = float(0.06)

# %% Initialize Grid class
class Grid:
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
