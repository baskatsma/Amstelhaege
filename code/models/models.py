"""
models.py

CODERS      Bas Katsma

USAGE       to-do
"""

# %% Initialize House class
class genericHouse:
    """
    Generic House class that contains functions that all the subclasses use
    """

    def __init__(self):
        print("genericHouse is made.")

    # To do: add positional functions, get value, etc. etc. etc.

# %% Eengezinswoning
class Eengezinswoning(genericHouse):
    def __init__(self, gridLength, gridDepth):
        self.houseType = "eengezinswoning"
        self.houseDimensions = (8, 8)       # (length, depth) tuple
        self.houseFreeArea = 2      # Vrijstand in meters
        self.houseValue = 285000
        self.houseValueIncrease = float(0.03)

# %% Bungalow
class Bungalow(genericHouse):
    def __init__(self, gridLength, gridDepth):
        self.houseType = "bungalow"
        self.houseDimensions = (10, 7.5)        # (length, depth) tuple
        self.houseFreeArea = 3      # Vrijstand in meters
        self.houseValue = 399000
        self.houseValueIncrease = float(0.04)

# %% Maison
class Maison(genericHouse):
    def __init__(self, gridLength, gridDepth):
        self.houseType = "maison"
        self.houseDimensions = (11, 10.5)       # (length, depth) tuple
        self.houseFreeArea = 6      # Vrijstand in meters
        self.houseValue = 610000
        self.houseValueIncrease = float(0.06)

# %% Initialize Grid class
class Grid:
    """
    Grid that contains all houses
    """

    def __init__(self, gridLength, gridDepth, maxHouses):
        self.gridLength = gridLength
        self.gridDepth = gridDepth
        self.maxHouses = maxHouses
        self.fractionEengezinswoningen = float(0.60)
        self.fractionBungalows = float(0.25)
        self.fractionMaisons = float(0.15)
