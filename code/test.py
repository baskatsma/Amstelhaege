# %% Import classes
from models.models import *

# Residential area size (either 20, 40 or 60 houses at max)
maxHouses = 20

# Grid dimensions in meters
gridLength = 180
gridDepth = 160

# Create grid instance
gridField = Grid(gridLength, gridDepth, maxHouses)
print("maxHouses on grid is: " + str(gridField.maxHouses))
print("fractionEengezinswoningen is: " + str(gridField.fractionEengezinswoningen))

# %% Test houses
a = Eengezinswoning(gridLength, gridDepth)
b = Bungalow(gridLength, gridDepth)
c = Maison(gridLength, gridDepth)

print("A is een " + a.type + " met afmetingen: ", a.houseDimensions)
print("De waarde van A is: " + str(a.value) + " euro")
print("A nieuwe waarde met extra vrijstand is:", a.calculateNewValue())

print("B is een " + b.type + " met afmetingen: ", b.houseDimensions)
print("De waarde van B is: " + str(b.value) + " euro")
print("B nieuwe waarde met extra vrijstand is:", b.calculateNewValue())

# %% Test woonwijk
residentialArea = []

for eengezinswoning in range(gridField.totalAmountEengezinswoningen):
    residentialArea.append(Eengezinswoning(gridLength, gridDepth))

for bungalow in range(gridField.totalAmountBungalows):
    residentialArea.append(Bungalow(gridLength, gridDepth))

for maison in range(gridField.totalAmountMaisons):
    residentialArea.append(Maison(gridLength, gridDepth))

for i in range(len(residentialArea)):
    print(residentialArea[i].type)
