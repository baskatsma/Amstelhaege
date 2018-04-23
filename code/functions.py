# %% Initialize grid
def createGrid(gridXlength, gridYlength):

    grid = []
    dot = "."
    for i in range(gridXlength):
        row = []
        grid.append(row)
        for j in range(gridYlength):
            row.append(dot)

    # grid[0][0] is linksboven
    # grid[Y]grid[X] scheme
    grid[5][1] = "A"
    for element in grid:
        print(element)
