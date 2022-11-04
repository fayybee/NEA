def makeGraphAdjacencyList(CircuitGrid):
    firstComponantCoord = findFirstComponentCoords(CircuitGrid) #change this so that it is a list of coords of all nodes instead of just the coords of the first
    adjacencyList = {}
    try:
        firstComponantRow = firstComponantCoord[0]
        firstComponantCol = firstComponantCoord[1]
        adjacencys = checkForAdjacencies(CircuitGrid,firstComponantRow,firstComponantCol)
    except:
        print("no components")

# change this so that it find the location of all components and returns a list of coordinates of all the components,
# use this information to make the adjacency list so that you make sure none are missing
def findFirstComponentCoords(array):
    for row in range(len(array)):
        for column in range(len(array[row])):
            if array[row][column] != "":
                return row,column


def checkForAdjacencies(array,row,col):
    pass

array= [
    ["","","","",""],
    ["","","","",""],
    ["","","","",""],
    ["","","","",""]
]

makeGraphAdjacencyList(array)