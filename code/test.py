# %% Import classes
from models.models import *
from functions import *

# Residential area size (either 20, 40 or 60 houses at max)
maxHouses = 20

# Grid dimensions in meters
gridXLength = 18
gridYLength = 16

# Create grid instance
gridField = Grid(gridXLength, gridYLength, maxHouses)
print("maxHouses on grid is: " + str(gridField.maxHouses))
print("fractionEengezinswoningen is: " + str(gridField.fractionEengezinswoningen))

# %% Test houses
a = Eengezinswoning(gridXLength, gridYLength)
b = Bungalow(gridXLength, gridYLength)
c = Maison(gridXLength, gridYLength)

createGrid(gridXLength, gridYLength)

print("A is een " + a.type + " met afmetingen:", a.houseDimensions)
print("De waarde van A is: " + str(a.value) + " euro")
print("A nieuwe waarde met extra vrijstand is:", a.calculateNewValue())

print("B is een " + b.type + " met afmetingen:", b.houseDimensions)
print("De waarde van B is: " + str(b.value) + " euro")
print("B nieuwe waarde met extra vrijstand is:", b.calculateNewValue())

# %% Create new woonwijk
residentialArea = []

# Out of the maxHouses houses, add 0.60 * maxHouses eengezinswoningen
for eengezinswoning in range(gridField.totalAmountEengezinswoningen):
    residentialArea.append(Eengezinswoning(gridXLength, gridYLength))

# Out of the maxHouses houses, add 0.25 * maxHouses bungalows
for bungalow in range(gridField.totalAmountBungalows):
    residentialArea.append(Bungalow(gridXLength, gridYLength))

# Out of the maxHouses houses, add 0.15 * maxHouses maisons
for maison in range(gridField.totalAmountMaisons):
    residentialArea.append(Maison(gridXLength, gridYLength))

# Print woonwijk huizen
for i in range(len(residentialArea)):
    print(residentialArea[i].type)

grid[0][0] = "E"
