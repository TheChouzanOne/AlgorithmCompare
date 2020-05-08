import graphics as gx
from GridNode import GridNode

class AlgorithmGrid:
    def __init__(self, nodesPerSide):
        self.nodesPerSide = nodesPerSide
        self.grid = self.getInitialGrid()

    def __str__(self):
        gridString = ""
        for row in self.grid:
            for cell in row:
                gridString += "%s "%cell
            gridString += '\n'

        return gridString

    def __iter__(self):
        self.iterCounter = 0
        return self

    def __next__(self):
        if self.iterCounter >= self.nodesPerSide:
            raise StopIteration
        nextItem = self.grid[self.iterCounter]
        self.iterCounter = self.iterCounter + 1
        return nextItem

    def __getitem__(self, index):
        return self.grid[index]

    def getInitialGrid(self):
        return [ [GridNode() for x in range(self.nodesPerSide)] for y in range(self.nodesPerSide) ]

        
