# %% Import classes
import numpy as np
from models.models import *
from models.templates import *
from functions import *

#
def main():

    # Get maxHouses
    maxHouses = defineMaxHouses()

    # Create grid instance
    gridField = Grid(gridXLength, gridYLength, maxHouses)
    #gridArray = gridField.drawGrid()

    # Access tuple values
    # print(maisonTemplate["houseDimensions"][1])

    # Create numpy grid (vertical, horizontal)
    d = np.zeros( (gridYLength,gridXLength) )

    # Test woonwijk
    residentialArea = []

    # Create new houses based on the grid requirements
    for eengezinswoning in range(gridField.totalAmountEengezinswoningen):
        residentialArea.append(House(**eengezinswoningTemplate))

    for bungalow in range(gridField.totalAmountBungalows):
        residentialArea.append(House(**bungalowTemplate))

    for maison in range(gridField.totalAmountMaisons):
        residentialArea.append(House(**maisonTemplate))

    # Update uniqueIDs
    for house in range(len(residentialArea)):
        residentialArea[house].uniqueID = house

    # Loop over all houses
    for house in range(len(residentialArea)):
        if residentialArea[house].type == "eengezinswoning":
            currentHouse = residentialArea[house]
            coordinates = currentHouse.getNewCoordinates()

            d[coordinates] = 2

        elif residentialArea[house].type == "bungalow":
            currentHouse = residentialArea[house]
            coordinates = currentHouse.getNewCoordinates()

            d[coordinates] = 3

        elif residentialArea[house].type == "maison":
            currentHouse = residentialArea[house]
            coordinates = currentHouse.getNewCoordinates()

            d[coordinates] = 4
        else:
            print("Wtf jongons")

    for row in d:
        print(row)

    # # Print test woonwijk
    # for i in range(len(residentialArea)):
    #     print(residentialArea[i].type, "|| uniqueID is:", residentialArea[i].uniqueID)


    # # Print test extra House functions
    # b = House(**eengezinswoningTemplate)
    # print("")
    # print("B is een " + b.type + " met afmetingen:", b.houseDimensions)
    # print("De waarde van B is: " + str(b.value) + " euro")
    # print("B nieuwe waarde met extra vrijstand (", b.extraFreeArea, "meter ) is:", b.calculateNewValue())

# %%
if __name__ == "__main__":
    main()