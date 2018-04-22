from models.models import *

# %% Eengezinswoning test
a = House("eengezinswoning")
a.initializeHouseType()

# Bungalow test
b = House("bungalow")
b.initializeHouseType()

# Maison test
c = House("maison")
c.initializeHouseType()

# %% Residential area size (either 20, 40 or 60 houses at max)
maxHouses = 20

# Grid dimensions in meters
gridLength = 180
gridDepth = 160

# Create grid instance
gridField = Grid(gridLength, gridDepth, maxHouses)
print(gridField.maxHouses)
print(gridField.fractionEengezinswoningen)
