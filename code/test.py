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

<<<<<<< HEAD
print(a)
print("A is een " + a.houseType + " met afmetingen: ", a.houseDimensions)
print("De waarde is: " + str(a.houseValue) + " euro")

print(b)
print("B is een " + b.houseType + " met afmetingen: ", b.houseDimensions)
print("De waarde is: " + str(b.houseValue) + " euro")
=======
print("a.houseType is: " + a.houseType + " || a.dimensions: ", end="")
print(a.houseDimensions)
print("a.houseValue is: " + str(a.houseValue) + " euro")
<<<<<<< HEAD
print(a.calculateNewValue)
=======
>>>>>>> e094e239fc9e5bbfdf307e9576e76d24d3518183
>>>>>>> a947b065d486a0de8bb2c2b49bebf320431e10ad
