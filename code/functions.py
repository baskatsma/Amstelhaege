from random import randint


# %% Initialize grid
def createGrid(gridXlength, gridYlength):

    # create empty grid and initialize dot
    grid = []
    dot = 0
<<<<<<< HEAD

    # iterate Xlength times and add empty array
=======
>>>>>>> 9d046621ad94e6177574b168b2bba609570570be
    for i in range(gridXlength):
        row = []
        grid.append(row)

        # add Ylength times a dot per array
        for j in range(gridYlength):
            row.append(dot)

    # grid[0][0] is linksboven
    # grid[Y]grid[X] scheme
<<<<<<< HEAD
    grid[randint(0,15)][randint(0,17)] = 1
    # grid[randint(0,15)][randint(0,17)] = 2
    # grid[randint(0,15)][randint(0,17)] = 3
=======
    grid[5][1] = "A"
>>>>>>> 9d046621ad94e6177574b168b2bba609570570be
    for element in grid:
        print(element)

# for x in range(10):
#   print (randint(1,21))
