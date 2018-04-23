# %% Import classes
from models.models import *
from functions import *

# Residential area size (either 20, 40 or 60 houses at max)
maxHouses = 20

# Grid dimensions in meters
gridXlength = 10
gridYlength = 10

# Create grid instance
gridField = Grid(gridXlength, gridYlength, maxHouses)
print("maxHouses on grid is: " + str(gridField.maxHouses))
print("fractionEengezinswoningen is: " + str(gridField.fractionEengezinswoningen))

# %% Test houses
a = Eengezinswoning(gridXlength, gridYlength)
b = Bungalow(gridXlength, gridYlength)
c = Maison(gridXlength, gridYlength)

createGrid(gridXlength, gridYlength)

print("A is een " + a.type + " met afmetingen: ", a.houseDimensions)
print("De waarde is: " + str(a.value) + " euro")
print("De nieuwe waarde met extra vrijstand is:", a.calculateNewValue())

print("B is een " + b.type + " met afmetingen: ", b.houseDimensions)
print("De waarde is: " + str(b.value) + " euro")
