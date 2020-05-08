import graphics as gx

from win32api import GetSystemMetrics
from AlgorithmGrid import AlgorithmGrid
from ViewConfiguration import getConfiguration

class MainWindow:

    NODES_PER_SIDE = 10
    WINDOW_NAME = "Algorithm comparator"

    ALGORITHMS = [
        'DFS',
        'BFS',
        'AStar'
    ]

    def __init__(self):
        self.width = int(GetSystemMetrics(0) * 0.9)
        self.height = int(GetSystemMetrics(1) * 0.9)
        self.setupModels()
        self.setupComponents()
        self.run()

    def setupModels(self):
        self.ALGORITHM_MODELS = { algorithm: AlgorithmGrid(self.NODES_PER_SIDE) for algorithm in self.ALGORITHMS }

    def setupComponents(self):
        self.config = getConfiguration(self.width, self.height, self.NODES_PER_SIDE)
        self.window = self.getWindow()
        
        for algorithm in self.ALGORITHMS:
            self.updateAlgorithmGridView(algorithm)

    def getWindow(self):
        return gx.GraphWin(self.WINDOW_NAME, self.width, self.height)

    def updateAlgorithmGridView(self, algorithm):
        background = self.getAlgorithmGridBackground(algorithm)
        background.draw(self.window)

        for row_index, row in enumerate(self.ALGORITHM_MODELS[algorithm]):
            for column_index, cell in enumerate(row):
                cellView = self.getAlgorithmGridCell(cell, algorithm, row_index, column_index)
                cellView.draw(self.window)


    def getAlgorithmGridBackground(self, algorithm):
        P1 = gx.Point(
            self.config['algorithmColumns'][algorithm]['xOffsetUL'],
            self.config['algorithmColumns'][algorithm]['yOffsetUL'],
        )
        P2 = gx.Point(
            self.config['algorithmColumns'][algorithm]['xOffsetLR'],
            self.config['algorithmColumns'][algorithm]['yOffsetLR'],
        )

        background = gx.Rectangle(P1, P2)
        background.setFill('black')

        return background

    def getAlgorithmGridCell(self, cell, algorithm, row, column):
        P1_X = self.config['algorithmColumns'][algorithm]['xOffsetUL'] + \
                self.config['algorithmNodes']['offset'] + \
                column * self.config['algorithmNodes']['size']
        P1_Y = self.config['algorithmColumns'][algorithm]['yOffsetUL'] + \
                self.config['algorithmNodes']['offset'] + \
                row * self.config['algorithmNodes']['size']

        P2_X = self.config['algorithmColumns'][algorithm]['xOffsetUL'] + \
                self.config['algorithmNodes']['offset'] + \
                self.config['algorithmNodes']['nodeSize'] + \
                column * self.config['algorithmNodes']['size']
        P2_Y = self.config['algorithmColumns'][algorithm]['yOffsetUL'] + \
                self.config['algorithmNodes']['offset'] + \
                self.config['algorithmNodes']['nodeSize'] + \
                row * self.config['algorithmNodes']['size']
        
        P1 = gx.Point(P1_X, P1_Y)
        P2 = gx.Point(P2_X, P2_Y)

        cellView = gx.Rectangle(P1, P2)
        cellView.setFill(cell.getColor())

        return cellView

    def run(self):
        while True:
            clickPoint = self.window.getMouse()
            self.handleClick(clickPoint)
        
        
    def handleClick(self, clickPoint):
        xClick, yClick = clickPoint.getX(), clickPoint.getY()

        # FIRST CHECK IF IT BELONGS TO AN ALGORITHM OR MORE MENU OPTIONS
        algorithm = self.getAlgorithmClicked(xClick)
        row, column = self.getCellClickedCoordinates(xClick, yClick, algorithm)
        for algorithm in self.ALGORITHMS:
            cell = self.ALGORITHM_MODELS[algorithm][row][column]
            cell.click()

            newCellView = self.getAlgorithmGridCell(cell, algorithm, row, column)
            newCellView.draw(self.window)

    def getAlgorithmClicked(self, xClick):
        algorithmColumn = int(xClick / (self.width / len(self.ALGORITHMS)))
        return self.ALGORITHMS[algorithmColumn]

    def getCellClickedCoordinates(self, xClick, yClick, algorithm):

        algorithmGridStartX = self.config['algorithmColumns'][algorithm]['xOffsetUL']
        algorithmGridStartY = self.config['algorithmColumns'][algorithm]['yOffsetUL']
        cellSize = self.config['algorithmNodes']['size']
        gridSize = self.config['algorithmColumns']['algorithmGridSize']

        column_index = int((xClick - algorithmGridStartX) / cellSize)
        row_index = int((yClick - algorithmGridStartY) / cellSize)

        return row_index, column_index
