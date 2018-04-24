# %% Import classes
import sys
from models.models import *
from functions import *

# Residential area size (either 20, 40 or 60 houses at max)
# 20 by default, unless specified
maxHouses = 20

if len(sys.argv) == 1:
    print("1 argument is used (only test.py)")
    print("maxHouses remains 20")

elif len(sys.argv) == 2:
    if str(sys.argv[1]) == "20":
        print("sys.argv = 20, maxHouses remains 20")
    elif str(sys.argv[1]) == "40":
        maxHouses = 40
        print("sys.argv = 40, maxHouses = 40")
    elif str(sys.argv[1]) == "60":
        maxHouses = 60
        print("sys.argv = 60, maxHouses = 60")
    else:
        maxHouses = 20
        print("sys.argv is an invalid number, maxHouses = 20 by default")

# Grid dimensions in meters
gridXLength = 18
gridYLength = 16

# Create grid instance
gridField = Grid(gridXLength, gridYLength, maxHouses)
print("maxHouses on grid is: " + str(gridField.maxHouses))
print("fractionEengezinswoningen is: " + str(gridField.fractionEengezinswoningen))
createGrid(gridXLength, gridYLength)

# %% Test houses
a = Eengezinswoning(gridXLength, gridYLength)
b = Bungalow(gridXLength, gridYLength)
c = Maison(gridXLength, gridYLength)

print("A is een " + a.type + " met afmetingen:", a.houseDimensions)
print("De waarde van A is: " + str(a.value) + " euro")
print("A nieuwe waarde met extra vrijstand is:", a.calculateNewValue())

print("B is een " + b.type + " met afmetingen:", b.houseDimensions)
print("De waarde van B is: " + str(b.value) + " euro")
print("B nieuwe waarde met extra vrijstand is:", b.calculateNewValue())

# %% Test woonwijk
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

for i in range(len(residentialArea)):
    print(residentialArea[i].type)
