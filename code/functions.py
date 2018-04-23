def createGrid(gridXlength, gridYlength):

    grid = []
    dot = "."
    for i in range(gridYlength):
        row = []
        grid.append(row)
        for j in range(gridXlength):
            row.append(dot)

    for element in grid:
        print(element)
