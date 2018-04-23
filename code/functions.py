# %% Initialize grid
def createGrid(gridXlength, gridYlength):

    grid = []
    dot = "."
    for i in range(gridXlength):
        row = []
        grid.append(row)
        for j in range(gridYlength):
            row.append(dot)

<<<<<<< HEAD
    grid[0][0] = "E"
=======
    # grid[0][0] is linksboven
    # grid[Y]grid[X] scheme
    grid[5][1] = "A"
>>>>>>> f6b20c4670fccaa21c29b79606b8d22065867ab8
    for element in grid:
        print(element)
