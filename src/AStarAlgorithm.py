from dataclasses import dataclass, field

from GridNode import GridNode
from Algorithm import Algorithm

from heapq import heappush, heappop

from itertools import count

class AStarAlgorithm(Algorithm):

    def __init__(self, algorithmGrid):
        self.grid = algorithmGrid

        # Please see https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes for more info on why this was needed
        self.counter = count()

    def _h(self, node):
        FINISH_NODE_ROW = self.grid.nodesPerSide - 1
        FINISH_NODE_COLUMN = self.grid.nodesPerSide - 1

        return abs(node.row - FINISH_NODE_ROW) + abs(node.column - FINISH_NODE_COLUMN)

    def _f(self, node, gValue):
        return gValue + self._h(node)

    def getName(self):
        return 'AStar'

    def runAlgorithm(self):
        finished = False
        pQueue = []
        startNode = self.grid[0][0]
        initialGValue = 0
        startNodeCost = self._f(startNode, initialGValue)
        heappush(pQueue, (startNodeCost, initialGValue, next(self.counter), startNode))

        isEmpty = lambda l: len(l) == 0

        while not isEmpty(pQueue):
            currentNodeCost, currentNodeGValue, _, currentNode = heappop(pQueue)
            currentNode.setState(GridNode.VISITED_STATE)

            if currentNode.isFinish():
                finished = True
                break

            neighbors = self._getNeighbors(currentNode)
            undiscoveredNeighbors = self._filterUndiscoveredNeighbors(neighbors)

            for undiscoveredNeighbor in undiscoveredNeighbors:
                undiscoveredNeighborGValue = currentNodeGValue + 1
                undiscoveredNeighborCost = self._f(undiscoveredNeighbor, undiscoveredNeighborGValue)

                heappush(pQueue, (undiscoveredNeighborCost, undiscoveredNeighborGValue, next(self.counter), undiscoveredNeighbor) )
                undiscoveredNeighbor.setState(GridNode.DISCOVERED_STATE)

            yield (False, self.IN_PROGRESS_STATE)
        
        if finished:
            yield (True, self.FINISH_STATE)
        else:
            yield (True, self.NO_SOLUTION_STATE)