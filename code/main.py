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

    # Create numpy grid (verticalY, horizontalX)
    buildingSite = np.zeros( (gridYLength,gridXLength) )

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

        # Draw all eengezinswoningen on grid
        if residentialArea[house].type == "eengezinswoning":
            currentHouse = residentialArea[house]

            currentHouse.drawOnGrid(buildingSite, currentHouse)

        # Draw all bungalows on grid
        elif residentialArea[house].type == "bungalow":
            currentHouse = residentialArea[house]

            currentHouse.drawOnGrid(buildingSite, currentHouse)

        # Draw all maisons on grid
        elif residentialArea[house].type == "maison":
            currentHouse = residentialArea[house]

            currentHouse.drawOnGrid(buildingSite, currentHouse)

    # Print build
    rowCounter = 0
    print("      X ---->")
    print("  Y ")
    for row in buildingSite:
        if rowCounter < 10:
            print(".",rowCounter," ", end="")
        else:
            print("",rowCounter," ", end="")

        print(row)
        rowCounter += 1

    # X, Y row
    # if np.any(buildingSite[1, :] == 2):
    #     print("2 is found on ANY of the X-rows: 1")
    #
    # if np.any(buildingSite[0:2, :] == 2):
    #     print("2 is found on ANY of the X-rows: 0, 1 and 2")

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
