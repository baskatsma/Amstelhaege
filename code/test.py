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
print("De waarde is: " + str(a.value) + " euro")

print("B is een " + b.type + " met afmetingen: ", b.houseDimensions)
print("De waarde is: " + str(b.value) + " euro")
