def makeGraphAdjacencyList(CircuitGrid):
    componantCoords = findComponentCoords(CircuitGrid)
    adjacencyList = {}
    for i in range(0, len(componantCoords)):
        row = str(componantCoords[i][0])
        col = str(componantCoords[i][1])
        adjacencyList[row + col] = checkForAdjacencies(CircuitGrid, int(row), int(col))
    print(adjacencyList)


def findComponentCoords(array):
    coordsList = []
    for row in range(len(array)):
        for column in range(len(array[row])):
            if array[row][column] != "":
                coordsList.append([row, column])
    return coordsList


def checkForAdjacencies(array, row, col):
    adjacentCoordsList = []
    # checks positions around the coordinate as long as there are not going to be off  the grid
    if row > 0:
        if array[row - 1][col] != "":
            adjacentCoordsList.append([row - 1, col])
    if col > 0:
        if array[row][col - 1] != "":
            adjacentCoordsList.append([row, col - 1])
    if row < (len(array) - 1):
        if array[row + 1][col] != "":
            adjacentCoordsList.append([row + 1, col])
    if col < (len(array[0])-1):
        if array[row][col+1] != "":
            adjacentCoordsList.append([row, col + 1])
    return adjacentCoordsList


# array = [
#     ["", "", "", "q", ""],
#     ["", "", "", "", ""],
#     ["", "", "", "", ""],
#     ["", "", "", "", ""]
# ]
#
# makeGraphAdjacencyList(array)
