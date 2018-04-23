def createGrid(gridXlength, gridYlength):

    grid = []
    row = []
    dot = "."
    for i in range(gridYlength):
        row = grid.append([])

        for j in range(gridXlength):
            row.append(dot)

    for element in grid:
        print(element)
