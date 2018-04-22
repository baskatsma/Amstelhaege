"""
houseModel.py

CODERS      Bas Katsma

USAGE       to-do
"""

class House:
    """
    House class that contains 3 types
    """

    def __init__(self, type):
        self.houseType = type
        self.houseDimensions = ()

    def initializeHouseType(self):

        # Dimensions in (length, depth) tuple format
        if self.houseType == "eengezinswoning":
            print("type is eengezinswoning!")
            self.houseDimensions = 8, 8
            print(self.houseDimensions)

        elif self.houseType == "bungalow":
            print("type is bungalow!")
            self.houseDimensions = 10, 7.5
            print(self.houseDimensions)

        elif self.houseType == "maison":
            print("type is maison!")
            self.houseDimensions = 11, 10.5
            print(self.houseDimensions)
