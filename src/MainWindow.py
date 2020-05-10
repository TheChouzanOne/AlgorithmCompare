import math
import graphics as gx
from time import sleep
from win32api import GetSystemMetrics

from ViewConfiguration import getConfiguration, getAlgorithmsInOrder

from AlgorithmGrid import AlgorithmGrid

from AlgorithmFactory import createAlgorithm
from Algorithm import Algorithm

class MainWindow:
    NODES_PER_SIDE = 30
    WINDOW_NAME = "Algorithm comparator"
    SECONDS_PER_STEP = 0.001

    def __init__(self):
        self.width = GetSystemMetrics(0) * 0.9
        self.height = GetSystemMetrics(1) * 0.7
        self.algorithmNames = getAlgorithmsInOrder()

        self.setupModels()
        self.setupComponents()
        self._run()

    def setupModels(self):
        self.algorithmModels = { 
            algorithm: AlgorithmGrid(
                self.width,
                self.height,
                self.NODES_PER_SIDE,
                algorithm
            ) for algorithm in self.algorithmNames
        }

    def setupComponents(self):
        self.window = self._getWindow()
        
        for algorithm in self.algorithmNames:
            self.algorithmModels[algorithm].draw(self.window)

    def _getWindow(self):
        window = gx.GraphWin(self.WINDOW_NAME, self.width, self.height)
        window.setBackground('lightgray')
        return window

    def _run(self):
        while True:
            clickPoint = self.window.getMouse()
            self._handleClick(clickPoint)
        
    def _handleClick(self, clickPoint):
        ## IF GRID CLICK
        xClick, yClick = clickPoint.getX(), clickPoint.getY()
        row, column = self._getCellClickedCoordinates(xClick, yClick)
        if(not (row < 0 or column < 0)):
            for algorithm in self.algorithmNames:
                cell = self.algorithmModels[algorithm][row][column]
                cell.click()
        else: ## IF START CLICK ---- NEEDS TO IMPLEMENT LOGIC
            self._runAlgorithms()

    def _runAlgorithms(self):

        algorithms = [
            createAlgorithm(algorithmName, self.algorithmModels[algorithmName]) for algorithmName in self.algorithmNames
        ]

        for algorithmResponses in zip(*[algorithm.run() for algorithm in algorithms]):
            allFinished = True
            for algorithmResponse in algorithmResponses:
                finished, state, algorithmName = algorithmResponse
                if finished:
                    if state == Algorithm.NO_SOLUTION_STATE:
                        self.algorithmModels[algorithmName].setBackgroundColor('red')
                    elif state == Algorithm.FINISH_STATE:
                        self.algorithmModels[algorithmName].setBackgroundColor('green')
                allFinished &= finished

            if allFinished:
                self.window.getMouse()
                self._resetAlgorithmsState()
                return

            sleep(self.SECONDS_PER_STEP)
    
    def _resetAlgorithmsState(self):
        for algorithm in self.algorithmNames:
            self.algorithmModels[algorithm].resetState()
            self.algorithmModels[algorithm].setBackgroundColor('black')


    def _getCellClickedCoordinates(self, xClick, yClick):
        config = getConfiguration(self.width, self.height, self.NODES_PER_SIDE, self.algorithmNames[0])
        cellSize = config['algorithmNodes']['size']
        
        XPositionInAlgorithmColumn = int(xClick) % int(config['algorithmColumns']['size'])
        XPositionInAlgorithmGrid = XPositionInAlgorithmColumn - config['algorithmColumns']['xOffsetUL']

        YPositionInAlgorithmGrid = yClick - config['algorithmColumns']['yOffsetUL']

        cellColumn = math.floor( XPositionInAlgorithmGrid / cellSize )
        cellRow = math.floor( YPositionInAlgorithmGrid / cellSize )

        if self._areInsideAlgorithmGrid(cellRow, cellColumn):
            return cellRow, cellColumn
        
        return -1, -1

    def _areInsideAlgorithmGrid(self, row, column):
        return column >= 0 and column < self.NODES_PER_SIDE and row >= 0 and row < self.NODES_PER_SIDE
