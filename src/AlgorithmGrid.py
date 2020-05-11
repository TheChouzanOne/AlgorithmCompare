from GridNode import GridNode
from AlgorithmGridView import AlgorithmGridView
from ViewConfiguration import getConfiguration

class AlgorithmGrid:
    def __init__(self, width, height, nodesPerSide, algorithm, startPosition = (0,0), finishPosition = None):
        self.nodesPerSide = nodesPerSide
        self.config = getConfiguration(width, height, nodesPerSide, algorithm)

        self.startPosition = startPosition
        self.finishPosition = finishPosition if finishPosition is not None else (nodesPerSide - 1, nodesPerSide - 1)
        
        self.grid = self._getInitialGrid()
        self.view = AlgorithmGridView(width, height, nodesPerSide, self.config)

    def __getitem__(self, index):
        return self.grid[index]

    def __str__(self):
        gridString = ''
        for row in self.grid:
            for cell in row:
                gridString += "%s "%cell
            gridString += "\n"

        return gridString

    def colorPath(self):
        finishRow = self.finishPosition[0]
        finishCol = self.finishPosition[1]
        FINISH_NODE = self.grid[finishRow][finishCol]

        iterNode = FINISH_NODE.parent

        while iterNode.parent is not None:
            iterNode.setPath()
            iterNode = iterNode.parent


    def setBackgroundColor(self, color):
        self.view.setBackgroundColor(color)

    def draw(self, window):
        self.view.draw(window)
        for row in self.grid:
            for cell in row:
                cell.draw(window)

    def resetState(self):
        for row in self.grid:
            for cell in row:
                cell.resetState()
        
    def _getInitialGrid(self):
        grid = [ 
            [
                GridNode(row, column, self.config) for column in range(self.nodesPerSide)
            ] for row in range(self.nodesPerSide)
        ]

        startRow = self.startPosition[0]
        startCol = self.startPosition[1]
        finishRow = self.finishPosition[0]
        finishCol = self.finishPosition[1]

        grid[startRow][startCol].setStart()
        grid[finishRow][finishCol].setFinish()

        return grid

    def getStartNode(self):
        startRow = self.startPosition[0]
        startCol = self.startPosition[1]

        return self.grid[startRow][startCol]
    


        
