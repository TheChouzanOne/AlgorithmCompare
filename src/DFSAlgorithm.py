from GridNode import GridNode

class DFSAlgorithm():
    name = 'DFS'

    NO_SOLUTION_STATE = 'no_solution'
    FINISH_STATE = 'finish'
    IN_PROGRESS_STATE = 'in_progress'

    def __init__(self, algorithmGrid):
        self.grid = algorithmGrid

    def run(self):
        finished = False
        stack = [self.grid[0][0]]

        isEmpty = lambda l: len(l) == 0

        while not isEmpty(stack):
            currentNode = stack.pop()
            currentNode.setState(GridNode.VISITED_STATE)

            if currentNode.isFinish():
                finished = True
            
            while finished:
                yield (True, self.FINISH_STATE)

            neighbors = self._getNeighbors(currentNode)
            undiscoveredNeighbors = self._filterUndiscoveredNeighbors(neighbors)

            for undiscoveredNeighbor in undiscoveredNeighbors:
                stack.append(undiscoveredNeighbor)
                undiscoveredNeighbor.setState(GridNode.DISCOVERED_STATE)

            yield (False, self.IN_PROGRESS_STATE)
        
        while True:
            yield (True, self.NO_SOLUTION_STATE)

    def _getNeighbors(self, gridNode):
        difference = [1, 0, -1]

        neighbors = []

        for rowDifference in difference:
            for columnDifference in difference:
                if not (rowDifference or columnDifference): # Diferrent than 0,0
                    continue 

                column = gridNode.column + columnDifference
                row = gridNode.row + rowDifference
                if not self._areValidRowColumn(column, row):
                    continue

                neighbors.append(self.grid[row][column])

        return neighbors

    def _filterUndiscoveredNeighbors(self, neighbors):
        return filter(lambda node: node.getState() == GridNode.UNDISCOVERED_STATE, neighbors)

    def _areValidRowColumn(self, column, row):
        return False if \
            column < 0 or column >= self.grid.nodesPerSide or \
            row < 0 or row >= self.grid.nodesPerSide \
            else True