from DFSAlgorithm import DFSAlgorithm
from BFSAlgorithm import BFSAlgorithm
from AStarAlgorithm import AStarAlgorithm

constructors = {
    'BFS' : BFSAlgorithm,
    'DFS' : DFSAlgorithm,
    'AStar' : AStarAlgorithm
}

def createAlgorithm(algorithmName, algorithmGrid):
    return constructors[algorithmName](algorithmGrid)