from GridNode import GridNode
from Algorithm import Algorithm

from queue import Queue

class BFSAlgorithm(Algorithm):

    def __init__(self, algorithmGrid):
        self.grid = algorithmGrid

    def getName(self):
        return 'BFS'

    def runAlgorithm(self):
        finished = False
        queue = Queue()
        queue.put(self.grid[0][0])

        while not queue.empty():
            currentNode = queue.get()
            currentNode.setState(GridNode.VISITED_STATE)

            if currentNode.isFinish():
                finished = True
                break

            neighbors = self._getNeighbors(currentNode)
            undiscoveredNeighbors = self._filterUndiscoveredNeighbors(neighbors)

            for undiscoveredNeighbor in undiscoveredNeighbors:
                queue.put(undiscoveredNeighbor)
                undiscoveredNeighbor.setState(GridNode.DISCOVERED_STATE)

            yield (False, self.IN_PROGRESS_STATE)
        
        if finished:
            yield (True, self.FINISH_STATE)
        else:
            yield (True, self.NO_SOLUTION_STATE)