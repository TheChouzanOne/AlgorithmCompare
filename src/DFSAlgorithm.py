from GridNode import GridNode
from Algorithm import Algorithm

class DFSAlgorithm(Algorithm):

    def __init__(self, algorithmGrid):
        self.grid = algorithmGrid

    def getName(self):
        return 'DFS'

    def runAlgorithm(self):
        finished = False
        stack = [self.grid.getStartNode()]

        isEmpty = lambda l: len(l) == 0

        while not isEmpty(stack):
            currentNode = stack.pop()
            currentNode.setState(GridNode.VISITED_STATE)

            if currentNode.isFinish():
                finished = True
                break

            neighbors = self._getNeighbors(currentNode)
            undiscoveredNeighbors = self._filterUndiscoveredNeighbors(neighbors)

            for undiscoveredNeighbor in undiscoveredNeighbors:
                stack.append(undiscoveredNeighbor)
                undiscoveredNeighbor.setParent(currentNode)
                undiscoveredNeighbor.setState(GridNode.DISCOVERED_STATE)

            yield (False, self.IN_PROGRESS_STATE)
        
        if finished:
            yield (True, self.FINISH_STATE)
        else:
            yield (True, self.NO_SOLUTION_STATE)