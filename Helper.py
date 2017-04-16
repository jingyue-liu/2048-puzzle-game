   
def move(grid, dir):
    

    if dir == 0:
        return moveUD(grid, False)
    if dir == 1:
        return moveUD(grid, True)
    if dir == 2:
        return moveLR(grid, False)
    if dir == 3:
        return moveLR(grid, True)            
        
def moveUD(grid, down):
    r = range(grid.size -1, -1, -1) if down else range(grid.size)

    moved = False

    for j in range(grid.size):
        cells = []

        for i in r:
            cell = grid.map[i][j]

            if cell != 0:
                cells.append(cell)

        grid.merge(cells)

        for i in r:
            value = cells.pop(0) if cells else 0

            if grid.map[i][j] != value:
                moved = True

            grid.map[i][j] = value

    return [moved,grid]

# move left or right
def moveLR(grid, right):
    r = range(grid.size - 1, -1, -1) if right else range(grid.size)

    moved = False

    for i in range(grid.size):
        cells = []

        for j in r:
            cell = grid.map[i][j]

            if cell != 0:
                cells.append(cell)

        grid.merge(cells)

        for j in r:
            value = cells.pop(0) if cells else 0

            if grid.map[i][j] != value:
                moved = True

            grid.map[i][j] = value

    return [moved,grid]
    
def getAvailableMoves(grid):
    availableMoves = []
    dirs = [0,1,2,3]
    for x in dirs:
        gridCopy = grid.clone()
        temp = move(gridCopy,x)
        if temp[0]:
            availableMoves.append([x,temp[1]])

    return availableMoves
    
    

