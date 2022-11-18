def makeGraphAdjacencyList(CircuitGrid):
    componentCoordinates = findComponentCoords(CircuitGrid)
    adjacencyList = {}
    for i in range(0, len(componentCoordinates)):
        row = str(componentCoordinates[i][0])
        col = str(componentCoordinates[i][1])
        adjacencyList[row + "," + col] = checkForAdjacencies(CircuitGrid, int(row), int(col))
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
    # rows are done first as opposed to normally column first so lists are horizontal
    if row > 0:
        if array[row - 1][col] != "":
            adjacentCoordsList.append(",".join([str(row - 1), str(col)]))
            # coords are converted to a string so it can be more easily used in graph traversals
    if col > 0:
        if array[row][col - 1] != "":
            adjacentCoordsList.append(",".join([str(row), str(col - 1)]))
    if row < (len(array) - 1):
        if array[row + 1][col] != "":
            adjacentCoordsList.append(",".join([str(row + 1), str(col)]))
    if col < (len(array[0]) - 1):
        if array[row][col + 1] != "":
            adjacentCoordsList.append(",".join([str(row), str(col + 1)]))
    return adjacentCoordsList


# def breakDownAdjacencyList(adjacencyList,node,stopnode):
#     visitedNodes = []
#     if node not in visitedNodes:
#         visitedNodes.append(node)
#         for neighbour in adjacencyList[node]:
#             if neighbour != stopnode:
#                 breakDownAdjacencyList()


