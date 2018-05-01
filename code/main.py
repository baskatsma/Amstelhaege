# %% Import classes
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from models.models import *
from models.templates import *
from functions import *

# Starting point
def main():

    # Get maxHouses
    maxHouses = defineMaxHouses()

    # Create grid instance
    gridField = Grid(gridXLength, gridYLength, maxHouses)

    # Create numpy grid (verticalY, horizontalX)
    numpyGrid = np.zeros((gridYLength,gridXLength),dtype=object)

    # Create woonwijk
    residentialArea = []

    # Create new houses based on the grid requirements
    for eengezinswoning in range(gridField.totalAmountEengezinswoningen):
        residentialArea.append(House(**eengezinswoningTemplate))

    for bungalow in range(gridField.totalAmountBungalows):
        residentialArea.append(House(**bungalowTemplate))

    for maison in range(gridField.totalAmountMaisons):
        residentialArea.append(House(**maisonTemplate))

    # Initialize total score
    totalScore = 0

    # Loop over all houses
    for house in range(len(residentialArea)):

        # Update uniqueIDs (starting at 10)
        residentialArea[house].uniqueID = house + 10

        # Place houses on grid and calculate total score
        currentHouse = residentialArea[house]
        currentHouse.drawOnGrid(numpyGrid)
        totalScore += currentHouse.calculateScore()

    print("The total score is:" , totalScore)

    # # Print numpyGrid with some fancy thaaangs
    # rowCounter = 0
    # print("")
    # print("")
    # print("        X →")
    # print("        ",end="")
    # for i in range(gridXLength):
    #     if i < 10:
    #         print(i," ",end="")
    #     else:
    #         print(i,"",end="")
    # print("")
    # print("  ↓ Y")
    # for row in numpyGrid:
    #     if rowCounter < 10:
    #         print("   ",rowCounter," ", end="")
    #     else:
    #         print("  ",rowCounter," ", end="")
    #
    #     print(row)
    #     rowCounter += 1
    # print("")
    # print("")

    plt.figure()

    xGridList = [0, gridXLength, gridXLength, 0, 0]
    yGridList = [0, 0, gridYLength, gridYLength, 0]
    plt.plot(xGridList, yGridList)

    # Loop over all houses
    for house in residentialArea:

        xCoordinates = [house.xBegin, house.xEnd,
        house.xEnd, house.xBegin, house.xBegin]

        yCoordinates = [house.yBegin, house.yBegin,
        house.yEnd, house.yEnd, house.yBegin]

        plt.plot(xCoordinates, yCoordinates)

    plt.show()

    # # Print test woonwijk
    # for i in range(len(residentialArea)):
    #     print(residentialArea[i].type, "|| uniqueID is:",
    #     residentialArea[i].uniqueID)

    # # Print test extra House functions
    # b = House(**eengezinswoningTemplate)
    # print("")
    # print("B is een " + b.type + " met afmetingen:", b.houseDimensions)
    # print("De waarde van B is: " + str(b.value) + " euro")
    # print("B nieuwe waarde met extra vrijstand (", b.extraFreeArea, "meter )
    # is:", b.calculateNewValue())

# %%
if __name__ == "__main__":
    main()
