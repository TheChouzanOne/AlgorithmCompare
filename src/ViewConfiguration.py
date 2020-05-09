def getConfiguration(width, height, nodesPerSide, algorithm):
    columnSize = width / 3
    algorithmGridSize = 0.8 * columnSize
    xOffset = (columnSize - algorithmGridSize) / 2
    yOffset = (height - algorithmGridSize) / 2
    windowColumn = getAlgorithmWindowColumn(algorithm)

    algorithmNodeSize = algorithmGridSize / nodesPerSide
    return {
        'algorithmColumns': {
            'size': columnSize,
            'algorithmGridSize': 0.8 * algorithmGridSize,
            'xOffsetUL': windowColumn * columnSize + xOffset,
            'yOffsetUL': yOffset,
            'xOffsetLR': windowColumn * columnSize + xOffset + algorithmGridSize,
            'yOffsetLR': yOffset + algorithmGridSize
        },
        'algorithmNodes': {
            'size': algorithmNodeSize,
            'nodeSize':  0.9 * algorithmNodeSize,
            'offset': 0.1 * algorithmNodeSize / 2
        }
    }

def getAlgorithmWindowColumn(algorithm):
    return getAlgorithmsInOrder().index(algorithm)

def getAlgorithmsInOrder():
    return [
        'DFS',
        'BFS',
        'AStar'
    ]