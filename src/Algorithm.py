from abc import ABCMeta, abstractmethod
from GridNode import GridNode

class Algorithm(metaclass=ABCMeta):

    NO_SOLUTION_STATE = 'no_solution'
    FINISH_STATE = 'finish'
    IN_PROGRESS_STATE = 'in_progress'
    IDLE_STATE = 'idle'

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def runAlgorithm(self) -> (bool, str):
        pass

    def run(self) -> (bool, str, str):
        for finished, state in self.runAlgorithm():
            yield (finished, state, self.getName())
            if finished:
                break
        while True:
            yield (True, self.IDLE_STATE, self.getName())


    def _getNeighbors(self, gridNode):
        difference = [1, 0, -1]

        neighbors = []

        for rowDifference in difference:
            for columnDifference in difference:
                if not (rowDifference or columnDifference): # FOR DIAGONAL MOVES
                    continue 
                # if not abs(rowDifference) + abs(columnDifference) == 1: # FOR ORTHOGONAL MOVES
                #     continue

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

    