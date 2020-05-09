from GridNode import GridNode

from AlgorithmGridView import AlgorithmGridView

from ViewConfiguration import getConfiguration

class AlgorithmGrid:
    def __init__(self, width, height, nodesPerSide, algorithm):
        self.nodesPerSide = nodesPerSide
        self.config = getConfiguration(width, height, nodesPerSide, algorithm)
        
        self.grid = self._getInitialGrid()
        self.view = AlgorithmGridView(width, height, nodesPerSide, self.config)

    # def __iter__(self):
    #     self.iterCounter = 0
    #     return self

    # def __next__(self):
    #     if self.iterCounter >= self.nodesPerSide:
    #         raise StopIteration
    #     nextItem = self.grid[self.iterCounter]
    #     self.iterCounter = self.iterCounter + 1
    #     return nextItem

    def draw(self, window):
        self.view.draw(window)
        for row in self.grid:
            for cell in row:
                cell.draw(window)
                

    def __getitem__(self, index):
        return self.grid[index]

    def _getInitialGrid(self):
        return [ 
            [
                GridNode(row, column, self.config) for column in range(self.nodesPerSide)
            ] for row in range(self.nodesPerSide)
        ]
    


        
