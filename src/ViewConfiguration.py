
def getConfiguration(width, height, nodesPerSide):
    columnSize = width / 3
    algorithmGridSize = 0.8 * columnSize
    xOffset = (columnSize - algorithmGridSize) / 2
    yOffset = (height - algorithmGridSize) / 2
    
    algorithmNodeSize = algorithmGridSize / nodesPerSide
    return {
        'algorithmColumns': {
            'size': columnSize,
            'algorithmGridSize': 0.8 * algorithmGridSize,
            'DFS': {
                'xOffsetUL': 0 * columnSize + xOffset,
                'yOffsetUL': yOffset,
                'xOffsetLR': 0 * columnSize + xOffset + algorithmGridSize,
                'yOffsetLR': yOffset + algorithmGridSize
            },
            'BFS': {
                'xOffsetUL': 1 * columnSize + xOffset,
                'yOffsetUL': yOffset,
                'xOffsetLR': 1 * columnSize + xOffset + algorithmGridSize,
                'yOffsetLR': yOffset + algorithmGridSize
            },
            'AStar': {
                'xOffsetUL': 2 * columnSize + xOffset,
                'yOffsetUL': yOffset,
                'xOffsetLR': 2 * columnSize + xOffset + algorithmGridSize,
                'yOffsetLR': yOffset + algorithmGridSize
            }
        },
        'algorithmNodes': {
            'size': algorithmNodeSize,
            'nodeSize':  0.9 * algorithmNodeSize,
            'offset': 0.1 * algorithmNodeSize / 2
        }
    }

