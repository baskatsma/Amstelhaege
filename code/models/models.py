"""
models.py

CODERS      Bas Katsma

USAGE       to-do
"""

# %% Initialize House class
class House:
    """
    House class that contains 3 types
    """

    # Usage: newHouse = House("bungalow"), for example
    def __init__(self, houseType):
        self.houseType = houseType
        self.houseDimensions = tuple()

    # Set dimensions based on the house type
    def initializeHouseType(self):

        # Dimensions in (length, depth) tuple format
        if self.houseType == "eengezinswoning":
            self.houseDimensions = (8, 8)

        elif self.houseType == "bungalow":
            self.houseDimensions = (10, 7.5)

        elif self.houseType == "maison":
            self.houseDimensions = (11, 10.5)

        print("houseType is: " + self.houseType + " || dimensions: ", end="")
        print(self.houseDimensions)

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
