from GridNode import GridNode
from AlgorithmGridView import AlgorithmGridView
from ViewConfiguration import getConfiguration
import json

class AlgorithmGrid:
    def __init__(self, width, height, nodesPerSide, algorithm, startPosition = (0,0), finishPosition = None, initialGrid=None):
        self.nodesPerSide = nodesPerSide
        self.config = getConfiguration(width, height, nodesPerSide, algorithm)

        self.startPosition = startPosition
        self.finishPosition = finishPosition if finishPosition is not None else (nodesPerSide - 1, nodesPerSide - 1)
        
        self.grid = self._getInitialGrid(initialGrid)
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

    def updateFinishPosition(self, row, col):
        currentRow, currentCol = self.finishPosition[0], self.finishPosition[1]
        self.grid[currentRow][currentCol].setFinish(False)
        self.finishPosition = (row, col)
        self.grid[row][col].setFinish()

    def setBackgroundColor(self, color):
        self.view.setBackgroundColor(color)

    def draw(self, window):
        self.view.draw(window)
        for row in self.grid:
            for cell in row:
                cell.draw(window)

    def undraw(self):
        self.view.undraw()
        for row in self.grid:
            for cell in row:
                cell.undraw()

    def resetState(self):
        for row in self.grid:
            for cell in row:
                cell.resetState()
        
    def _getInitialGrid(self, initialGrid):
        grid = [ 
            [
                GridNode(row, column, self.config) for column in range(self.nodesPerSide)
            ] for row in range(self.nodesPerSide)
        ]

        if initialGrid is not None:
            for row in range(self.nodesPerSide):
                for col in range(self.nodesPerSide):
                    if initialGrid[row][col] == 'W':
                        grid[row][col].setState(GridNode.WALL_STATE)

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
    
    def toJson(self):
        jsonDict = {
            'nodesPerSide': self.nodesPerSide,
            'startPosition': self.startPosition,
            'finishPosition': self.finishPosition
        }

        grid = [
            ['W' if cell.isWall() \
                else 'U' \
                for cell in row
            ] for row in self.grid
        ]

        jsonDict['grid'] = grid

        return json.dumps(jsonDict)




        
