from random import randint

# %% Initialize grid
def createGrid(gridXlength, gridYlength):

    # create empty grid and initialize dot
    grid = []
    dot = 0

    # iterate Xlength times and add empty array
    for i in range(gridXlength):
        row = []
        grid.append(row)

        # add Ylength times a dot per array
        for j in range(gridYlength):
            row.append(dot)

    # grid[0][0] is linksboven
    # grid[Y]grid[X] scheme

    placeOnGrid(grid)

    for element in grid:
        print(element)

def placeOnGrid(grid):
    grid[randint(0,15)][randint(0,17)] = 1
    grid[randint(0,17)][randint(0,15)] = 2
