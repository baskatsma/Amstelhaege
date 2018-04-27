# %% Import classes
import numpy as np
from models.models import *
from functions2 import *

# Get maxHouses
maxHouses = defineMaxHouses()

# Grid dimensions in meters
gridXLength = 18
gridYLength = 16

# Define house templates (in dictionary format) to create class instances
eengezinswoningTemplate = {"type": "eengezinswoning",
                            "houseDimensions": (8, 8),
                            "freeArea": 2,
                            "extraFreeArea": 5,
                            "value": 285000,
                            "valueIncrease": float(0.03),
                            "positionX": 0,
                            "positionY": 0,
                            "gridXLength": gridXLength,
                            "gridYLength": gridYLength,
                            "uniqueID": 0}

bungalowTemplate = {"type": "bungalow",
                    "houseDimensions": (10, 7.5),
                    "freeArea": 3,
                    "extraFreeArea": 0,
                    "value": 399000,
                    "valueIncrease": float(0.04),
                    "positionX": 0,
                    "positionY": 0,
                    "gridXLength": gridXLength,
                    "gridYLength": gridYLength,
                    "uniqueID": 0}

maisonTemplate = {"type": "maison",
                    "houseDimensions": (11, 10.5),
                    "freeArea": 6,
                    "extraFreeArea": 0,
                    "value": 610000,
                    "valueIncrease": float(0.06),
                    "positionX": 0,
                    "positionY": 0,
                    "gridXLength": gridXLength,
                    "gridYLength": gridYLength,
                    "uniqueID": 0}

# Create grid instance
gridField = Grid(gridXLength, gridYLength, maxHouses)
gridArray = gridField.drawGrid()

# Create numpy grid (vertical, horizontal)
d = np.zeros( (16,18) )
# print(d)

# %% Test woonwijk
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

# Print test woonwijk
for i in range(len(residentialArea)):
    print(residentialArea[i].type, "|| uniqueID is:", residentialArea[i].uniqueID)

# Print test extra House functions
b = House(**eengezinswoningTemplate)
print("")
print("B is een " + b.type + " met afmetingen:", b.houseDimensions)
print("De waarde van B is: " + str(b.value) + " euro")
print("B nieuwe waarde met extra vrijstand (", b.extraFreeArea, "meter ) is:", b.calculateNewValue())









# # Out of the maxHouses houses, add 0.60 * maxHouses eengezinswoningen
# for eengezinswoning in range(gridField.totalAmountEengezinswoningen):
#     residentialArea.append(Eengezinswoning(gridXLength, gridYLength))
#
# # Out of the maxHouses houses, add 0.25 * maxHouses bungalows
# for bungalow in range(gridField.totalAmountBungalows):
#     residentialArea.append(Bungalow(gridXLength, gridYLength))
#
# # Out of the maxHouses houses, add 0.15 * maxHouses maisons
# for maison in range(gridField.totalAmountMaisons):
#     residentialArea.append(Maison(gridXLength, gridYLength))
