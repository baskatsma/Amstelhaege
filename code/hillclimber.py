# %% Import classes
import matplotlib.pyplot as plt
import random as rd
from models.models import *
from models.templates import *
from functions import *

def main():

    # Get maxHouses
    maxHouses = defineMaxHouses()

    # Create grid instance
    gridInformation = GridInformation(gridXLength, gridYLength, maxHouses)

    # Create numpy grid (verticalY, horizontalX)
    numpyGrid = np.zeros((gridYLength,gridXLength),dtype=object)

    # Create woonwijk
    residentialArea = []

    # Create new houses based on the grid requirements
    for eengezinswoning in range(gridInformation.totalAmountEengezinswoningen):
        residentialArea.append(House(**eengezinswoningTemplate))

    for bungalow in range(gridInformation.totalAmountBungalows):
        residentialArea.append(House(**bungalowTemplate))

    for maison in range(gridInformation.totalAmountMaisons):
        residentialArea.append(House(**maisonTemplate))

    # Initialize current and new score
    currentScore = 0
    newScore = 0

    # Loop over all houses
    for house in range(len(residentialArea)):

        # Give the current house an easy variable
        currentHouse = residentialArea[house]

        # Update uniqueIDs (starting at 10)
        currentHouse.uniqueID = house + 10

        # Place houses on grid and calculate total score
        currentHouse.drawOnGrid(numpyGrid)
        currentScore += currentHouse.calculateScore()

    print("The current score is:", currentScore)

    randomHouse1 = residentialArea[rd.randint(0,len(residentialArea))]
    randomHouse2 = residentialArea[rd.randint(0,len(residentialArea))]

    coordinates1 = (randomHouse1.yBegin, randomHouse1.xBegin)
    coordinates2 = (randomHouse2.yBegin, randomHouse2.xBegin)

    randomHouse1.yBegin = coordinates2[0]
    randomHouse1.xBegin = coordinates2[1]
    randomHouse2.yBegin = coordinates1[0]
    randomHouse2.xBegin = coordinates1[1]

    randomHouse1.drawOnGrid(numpyGrid)
    randomHouse2.drawOnGrid(numpyGrid)

    for house in range(len(residentialArea)):
        newScore = currentHouse.calculateScore()

    print("The new score is:", newScore)

    # if currentScore > newScore:



    # Initialize matplotlib
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

        if house.type == "eengezinswoning":
            ePlot = plt.plot(xCoordinates, yCoordinates)
            ePlot[0].set_color('r')

        elif house.type == "bungalow":
            bPlot = plt.plot(xCoordinates, yCoordinates)
            bPlot[0].set_color('g')

        elif house.type == "maison":
            mPlot = plt.plot(xCoordinates, yCoordinates)
            mPlot[0].set_color('y')

    # Show matplotlib
    plt.show()

# %%
if __name__ == "__main__":
    main()
