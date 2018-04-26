# %% Hydrogen run
import sys
#from random import randint

# %% Define residential area size (either 20, 40 or 60 houses at max)
def defineMaxHouses():

    # 20 by default, unless specified
    maxHouses = 20

    # Check if a number is entered in the CLI
    if len(sys.argv) == 1:
        print("1 argument is used (only test.py)")
        print("maxHouses remains 20")

    # Check if the number is valid (either 20, 40 or 60)
    elif len(sys.argv) == 2:
        if str(sys.argv[1]) == "20":
            print("sys.argv = 20, maxHouses remains 20")
        elif str(sys.argv[1]) == "40":
            maxHouses = 40
            print("sys.argv = 40, maxHouses = 40")
        elif str(sys.argv[1]) == "60":
            maxHouses = 60
            print("sys.argv = 60, maxHouses = 60")
        # Else default to 20
        else:
            maxHouses = 20
            print("sys.argv is an invalid number, maxHouses = 20 by default")

    return maxHouses

    placeOnGrid(grid)

    for element in grid:
        print(element)

# %% Place on grid function
def placeOnGrid(grid):

    eengezinswoning = 1
    bungalow = 2
    maison = 3

    location1Y = randint(-1,17)
    location1X = randint(-1,15)
    location2Y = randint(-1,17)
    location2X = randint(-1,15)
    location3Y = randint(-1,17)
    location3X = randint(-1,15)

    grid[location1Y][location1X] = eengezinswoning
    grid[location2Y][location2X] = bungalow
    grid[location3Y][location3X] = maison

    if not grid[location1Y][location1X] == grid[location2Y][location2X]:
        grid[location1Y][location1X] = eengezinswoning
        grid[location2Y][location2X] = bungalow
        grid[location3Y][location3X] = maison

# while True:
    # if locationEengezins == locationBungalow:
    #     locationEengezins = [randint(-1,17)][randint(-1,15)]
    # elif locationEengezins == locationMaison:
    #     locationEengezins = [randint(-1,17)][randint(-1,15)]
    # elif locationBungalow == locationMaison:
    #     locationBungalow = [randint(-1,17)][randint(-1,15)]
    # else:

# # %% Initialize grid
# def createGrid(gridXLength, gridYLength):
#
#     # Create empty grid and initialize dot
#     grid = []
#     dot = 0
#
#     # iterate Xlength times and add empty array
#     for i in range(gridXlength):
#         row = []
#         grid.append(row)
#
#         # add Ylength times a dot per array
#         for j in range(gridYlength):
#             row.append(dot)
#
#     # grid[0][0] is linksboven
#     # grid[Y]grid[X] scheme
#
#     placeOnGrid(grid)
#
#     for element in grid:
#         print(element)
#
#     return grid
#
# # %% Place on grid function
# def placeOnGrid(grid):
#
#     eengezinswoning = 1
#     bungalow = 2
#     maison = 3
#
#     grid[randint(-1,17)][randint(-1,15)] = eengezinswoning
#     grid[randint(-1,17)][randint(-1,15)] = bungalow
#     grid[randint(-1,17)][randint(-1,15)] = maison
