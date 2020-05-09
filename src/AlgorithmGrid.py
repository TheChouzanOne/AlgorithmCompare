from GridNode import GridNode
from AlgorithmGridView import AlgorithmGridView
from ViewConfiguration import getConfiguration

class AlgorithmGrid:
    def __init__(self, width, height, nodesPerSide, algorithm):
        self.nodesPerSide = nodesPerSide
        self.config = getConfiguration(width, height, nodesPerSide, algorithm)
        
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
                if cell.isWall():
                    continue
                cell.setState(GridNode.UNDISCOVERED_STATE)

    def _getInitialGrid(self):
        grid = [ 
            [
                GridNode(row, column, self.config) for column in range(self.nodesPerSide)
            ] for row in range(self.nodesPerSide)
        ]

        grid[0][0].setStart()
        grid[self.nodesPerSide-1][self.nodesPerSide-1].setFinish()

        return grid
    


        
