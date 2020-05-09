import math

import graphics as gx

from win32api import GetSystemMetrics
from AlgorithmGrid import AlgorithmGrid
from ViewConfiguration import getConfiguration, getAlgorithmsInOrder

from DFSAlgorithm import DFSAlgorithm
from BFSAlgorithm import BFSAlgorithm

from time import sleep

class MainWindow:

    NODES_PER_SIDE = 15
    WINDOW_NAME = "Algorithm comparator"
    SECONDS_PER_STEP = 0.05

    def __init__(self):
        self.width = GetSystemMetrics(0) * 0.9
        self.height = GetSystemMetrics(1) * 0.7
        self.algorithms = getAlgorithmsInOrder()

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
            ) for algorithm in self.algorithms
        }

    def setupComponents(self):
        self.window = self._getWindow()
        
        for algorithm in self.algorithms:
            self.algorithmModels[algorithm].draw(self.window)

    def _getWindow(self):
        return gx.GraphWin(self.WINDOW_NAME, self.width, self.height)

    def _run(self):
        while True:
            clickPoint = self.window.getMouse()
            self._handleClick(clickPoint)
        
    def _handleClick(self, clickPoint):
        ## IF GRID CLICK
        xClick, yClick = clickPoint.getX(), clickPoint.getY()
        row, column = self._getCellClickedCoordinates(xClick, yClick)
        if(not (row < 0 or column < 0)):
            for algorithm in self.algorithms:
                cell = self.algorithmModels[algorithm][row][column]
                cell.click()
        else: ## IF START CLICK ---- NEEDS TO IMPLEMENT LOGIC
            self._runAlgorithms()

    def _runAlgorithms(self):
        DFS = DFSAlgorithm(self.algorithmModels['DFS'])
        BFS = BFSAlgorithm(self.algorithmModels['BFS'])
        for dfsResponse, bfsResponse in zip(DFS.run(), BFS.run()):
            dfsFinished, dfsState = dfsResponse
            bfsFinished, bfsState = bfsResponse
            if dfsFinished:
                if dfsState == DFSAlgorithm.NO_SOLUTION_STATE:
                    self.algorithmModels['DFS'].setBackgroundColor('red')
                elif dfsState == DFSAlgorithm.FINISH_STATE:
                    self.algorithmModels['DFS'].setBackgroundColor('green')
            if bfsFinished:
                if bfsState == BFSAlgorithm.NO_SOLUTION_STATE:
                    self.algorithmModels['BFS'].setBackgroundColor('red')
                elif bfsState == BFSAlgorithm.FINISH_STATE:
                    self.algorithmModels['BFS'].setBackgroundColor('green')
            if all([dfsFinished, bfsFinished]):
                self.window.getMouse()
                self._resetAlgorithmsState()
                return
            sleep(self.SECONDS_PER_STEP)
    
    def _resetAlgorithmsState(self):
        for algorithm in self.algorithms:
            self.algorithmModels[algorithm].resetState()
            self.algorithmModels[algorithm].setBackgroundColor('black')


    def _getCellClickedCoordinates(self, xClick, yClick):
        config = getConfiguration(self.width, self.height, self.NODES_PER_SIDE, self.algorithms[0])
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
