import math
import json

import graphics as gx
from time import sleep
from win32api import GetSystemMetrics

from ViewConfiguration import getConfiguration, getAlgorithmsInOrder

from Button import Button
from NumberInput import NumberInput
from InstructionsText import Instructions

from AlgorithmGrid import AlgorithmGrid
from AlgorithmFactory import createAlgorithm
from Algorithm import Algorithm
from GridJsonSerializer import GridJsonSerializer

from tkinter.filedialog import asksaveasfilename, askopenfilename 

class MainWindow:
    nodesPerSide = 15
    WINDOW_NAME = "Algorithm comparator"
    SECONDS_PER_STEP = 0.001

    WALL_INSTRUCTIONS = "Click on grid to add walls or use the buttons"

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
                algorithm
            ) for algorithm in self.algorithmNames
        }

    def _setupComponents(self):
        self.window = self._getWindow()

        self._setupGrids()
        self._setupStartButton()
        self._setupSaveButton()
        self._setupLoadButton()
        self._setupChangeFinishButton()
        self._setupChangeStartButton()
        self._setupInstructions()
        self._setupUpdateGridSizeEntry()

    def _setupGrids(self):
        for algorithm in self.algorithmNames:
            self.algorithmModels[algorithm].draw(self.window)

    def _setupInstructions(self):
        position = (
            self.width / 2,
            self.height * 0.8 / 10
        )

        self.instructions = Instructions(
            self.WALL_INSTRUCTIONS, 
            position
        )

        self.instructions.draw(self.window)

    def _setupStartButton(self):
        size = self._getButtonSize()
        position = self._getButtonPosition(size, 0)

        self.startButton = Button('Run algorithms', 'gray', position, size, self._runAlgorithms)
        self.startButton.draw(self.window)

    def _setupSaveButton(self):
        size = self._getButtonSize()
        position = self._getButtonPosition(size, 1)

        self.saveButton = Button('Save maze', 'gray', position, size, self._saveMaze)
        self.saveButton.draw(self.window)

    def _setupLoadButton(self):
        size = self._getButtonSize()
        position = self._getButtonPosition(size, 2)

        self.loadButton = Button('Load maze', 'gray', position, size, self._loadMaze)
        self.loadButton.draw(self.window)

    def _setupChangeFinishButton(self):
        size = self._getButtonSize()
        position = self._getButtonPosition(size, -1)

        self.changeFinishButton = Button('Change finish\n cell', 'red', position, size, self._changeFinishNode)
        self.changeFinishButton.draw(self.window)

    def _setupChangeStartButton(self):
        size = self._getButtonSize()
        position = self._getButtonPosition(size, -2)

        self.changeStartButton = Button('Change start\n cell', 'yellow', position, size, self._changeStartNode)
        self.changeStartButton.draw(self.window)

    def _setupUpdateGridSizeEntry(self):
        size = self._getButtonSize()
        position = self._getButtonPosition(size, -4)

        self.updateGridSizeEntry = NumberInput(position, size, self._updateGridSize, defaultNumber = self.nodesPerSide, text = "Maze size")
        self.updateGridSizeEntry.draw(self.window)

    def _getButtonSize(self):
        return (
            self.width / 10,
            self.height / 10
        )

    def _getButtonPosition(self, size, offSetFromCenter):
        return (
            (self.width - size[0]) / 2 + offSetFromCenter * (size[0] + 10),
            13 * self.height / 15
        )

    def _changeFinishNode(self):
        instructionsText = "Click on a node to change the finish node"
        self.instructions.setText(instructionsText)

        row, column = self._getGridClickCoordinates()
        
        for algorithm in self.algorithmNames:
            self.algorithmModels[algorithm].updateFinishPosition(row, column)

        self.instructions.setText(self.WALL_INSTRUCTIONS)

    def _changeStartNode(self):
        instructionsText = "Click on a node to change the start node"
        self.instructions.setText(instructionsText)

        row, column = self._getGridClickCoordinates()
        
        for algorithm in self.algorithmNames:
            self.algorithmModels[algorithm].updateStartPosition(row, column)

        self.instructions.setText(self.WALL_INSTRUCTIONS)

    def _getGridClickCoordinates(self):
        while(True):
            mouseClick = self.window.getMouse()
            xClick, yClick = mouseClick.getX(), mouseClick.getY()
            row, column = self._getCellClickedCoordinates(xClick, yClick)
            if row != -1 and column != -1:
                break
        
        return row, column

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
        elif self.changeStartButton.isClicked(xClick, yClick):
            self.changeStartButton.click()
        elif self.updateGridSizeEntry.isClicked(xClick, yClick):
            self.updateGridSizeEntry.click()
        else:
            row, column = self._getCellClickedCoordinates(xClick, yClick)
            if(not (row < 0 or column < 0)):
                for algorithm in self.algorithmNames:
                    cell = self.algorithmModels[algorithm][row][column]
                    cell.click()

    def undrawGrids(self):
        for algorithm in self.algorithmNames:
            self.algorithmModels[algorithm].undraw()

    def _updateGridSize(self):
        self.undrawGrids()
        self.nodesPerSide = self.updateGridSizeEntry.getNumber()

        self.algorithmModels = { 
            algorithm: AlgorithmGrid(
                self.width,
                self.height,
                self.nodesPerSide,
                algorithm
            ) for algorithm in self.algorithmNames
        }

        self._setupGrids()

    def _loadMaze(self):
        jsonGrid = GridJsonSerializer.loadFile()
        
        if jsonGrid is None:
            return

        self.undrawGrids()
        self.nodesPerSide = jsonGrid['nodesPerSide']

        self.algorithmModels = { 
            algorithm: AlgorithmGrid(
                self.width,
                self.height,
                self.nodesPerSide,
                algorithm,
                jsonGrid['startPosition'],
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
                self.instructions.setText("Click anywhere to reset algorithms")
                self.window.getMouse()
                self._resetAlgorithmsState()
                self.instructions.setText(self.WALL_INSTRUCTIONS)
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
