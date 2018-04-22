"""
houseModel.py

CODERS      Bas Katsma

USAGE       to-do
"""

class House:
    """
    House class that contains 3 types
    """

    # Usage: newHouse = House("bungalow"), for example
    def __init__(self, type):
        self.houseType = type
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
