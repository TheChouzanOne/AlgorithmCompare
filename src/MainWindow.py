import math
import json

import graphics as gx
from time import sleep
from win32api import GetSystemMetrics

from ViewConfiguration import getConfiguration, getAlgorithmsInOrder
from Button import Button
from AlgorithmGrid import AlgorithmGrid
from AlgorithmFactory import createAlgorithm
from Algorithm import Algorithm
from GridJsonSerializer import GridJsonSerializer

from tkinter.filedialog import asksaveasfilename, askopenfilename 

class MainWindow:
    nodesPerSide = 15
    WINDOW_NAME = "Algorithm comparator"
    SECONDS_PER_STEP = 0.001

    initialPosition = (3, 7)

    def __init__(self):
        self.width = GetSystemMetrics(0) * 0.9
        self.height = GetSystemMetrics(1) * 0.7
        self.algorithmNames = getAlgorithmsInOrder()

        self.setupModels()
        self._setupComponents()
        self._run()

    def setupModels(self):
        self.algorithmModels = { 
            algorithm: AlgorithmGrid(
                self.width,
                self.height,
                self.nodesPerSide,
                algorithm,
                self.initialPosition
            ) for algorithm in self.algorithmNames
        }

    def _setupComponents(self):
        self.window = self._getWindow()

        self._setupGrids()
        self._setupStartButton()
        self._setupSaveButton()
        self._setupLoadButton()
        self._setupChangeFinishButton()

    def _setupGrids(self):
        for algorithm in self.algorithmNames:
            self.algorithmModels[algorithm].draw(self.window)

    def _setupStartButton(self):
        size = (
            self.width / 10,
            self.height / 10
        )

        position = (
            (self.width - size[0]) / 2,
            13 * self.height / 15
        )

        self.startButton = Button('Run algorithms', 'gray', position, size, self._runAlgorithms)
        self.startButton.draw(self.window)

    def _setupSaveButton(self):
        size = (
            self.width / 10,
            self.height / 10
        )

        position = (
            (self.width - size[0]) / 2 + size[0] + 10,
            13 * self.height / 15
        )

        self.saveButton = Button('Save maze', 'gray', position, size, self._saveMaze)
        self.saveButton.draw(self.window)

    def _setupLoadButton(self):
        size = (
            self.width / 10,
            self.height / 10
        )

        position = (
            (self.width - size[0]) / 2 + 2 * (size[0] + 10),
            13 * self.height / 15
        )

        self.loadButton = Button('Load maze', 'gray', position, size, self._loadMaze)
        self.loadButton.draw(self.window)

    def _setupChangeFinishButton(self):
        size = (
            self.width / 10,
            self.height / 10
        )

        position = (
            (self.width - size[0]) / 2 - (size[0] + 10),
            13 * self.height / 15
        )

        self.changeFinishButton = Button('Change finish\n cell', 'red', position, size, self._changeFinishNode)
        self.changeFinishButton.draw(self.window)

    def _changeFinishNode(self):
        while(True):
            mouseClick = self.window.getMouse()
            xClick, yClick = mouseClick.getX(), mouseClick.getY()
            row, column = self._getCellClickedCoordinates(xClick, yClick)
            if row != -1 and column != -1:
                break
        
        for algorithm in self.algorithmNames:
            self.algorithmModels[algorithm].updateFinishPosition(row, column)

    def _getWindow(self):
        window = gx.GraphWin(self.WINDOW_NAME, self.width, self.height)
        window.setBackground('lightgray')
        return window

    def _run(self):
        while True:
            clickPoint = self.window.getMouse()
            self._handleClick(clickPoint)
        
    def _handleClick(self, clickPoint):
        xClick, yClick = clickPoint.getX(), clickPoint.getY()
        if self.startButton.isClicked(xClick, yClick):
            self.startButton.click()
        elif self.loadButton.isClicked(xClick, yClick):
            self.loadButton.click()
        elif self.saveButton.isClicked(xClick, yClick):
            self.saveButton.click()
        elif self.changeFinishButton.isClicked(xClick, yClick):
            self.changeFinishButton.click()
        else:
            row, column = self._getCellClickedCoordinates(xClick, yClick)
            if(not (row < 0 or column < 0)):
                for algorithm in self.algorithmNames:
                    cell = self.algorithmModels[algorithm][row][column]
                    cell.click()

    def _loadMaze(self):
        jsonGrid = GridJsonSerializer.loadFile()
        
        if jsonGrid is None:
            return

        for algorithm in self.algorithmNames:
            self.algorithmModels[algorithm].undraw()

        self.nodesPerSide = jsonGrid['nodesPerSide']
        self.initialPosition = jsonGrid['startPosition']

        self.algorithmModels = { 
            algorithm: AlgorithmGrid(
                self.width,
                self.height,
                self.nodesPerSide,
                algorithm,
                self.initialPosition,
                jsonGrid['finishPosition'],
                jsonGrid['grid']
            ) for algorithm in self.algorithmNames
        }

        self._setupGrids()

    def _saveMaze(self):
        anyAlgorithm = self.algorithmNames[0]
        anyGrid = self.algorithmModels[anyAlgorithm]
        GridJsonSerializer.saveToJson(anyGrid)
        

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
                        self.algorithmModels[algorithmName].colorPath()
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
        config = getConfiguration(self.width, self.height, self.nodesPerSide, self.algorithmNames[0])
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
        return column >= 0 and column < self.nodesPerSide and row >= 0 and row < self.nodesPerSide
