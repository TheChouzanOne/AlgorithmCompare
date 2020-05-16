from GridNodeView import GridNodeView

class GridNode:
    WALL_STATE = 'wall'
    UNDISCOVERED_STATE = 'undiscovered'
    DISCOVERED_STATE = 'discovered'
    VISITED_STATE = 'visited'

    WALL_SPACE_COLOR = 'black'
    UNDISCOVERED_SPACE_COLOR = 'lightgray'
    DISCOVERED_SPACE_COLOR = 'gray'
    VISITED_SPACE_COLOR = 'blue'
    START_SPACE_COLOR = 'yellow'
    FINISH_SPACE_COLOR = 'red'
    PATH_SPACE_COLOR = 'purple'

    def __init__(self, row, column, config):
        self.row = row
        self.column = column
        self.state = self.UNDISCOVERED_STATE
        self.start = False
        self.finish = False
        self.path = False
        self.parent = None
        
        self.view = GridNodeView(row, column, self.UNDISCOVERED_SPACE_COLOR, config)

    def __str__(self):
        return 's' if self.isStart() else \
            'f' if self.isFinish() else \
            self.getState()[0]

    def isWall(self):
        return self.state == self.WALL_STATE

    def _makeWall(self):
        self.view.setColor(self.WALL_SPACE_COLOR)

    def _makeUndiscoveredSpace(self):
        self.view.setColor(self.UNDISCOVERED_SPACE_COLOR)

    def _makeDiscoveredSpace(self):
        self.view.setColor(self.DISCOVERED_SPACE_COLOR)

    def _makeVisitedSpace(self):
        self.view.setColor(self.VISITED_SPACE_COLOR)

    def _makeStartSpace(self):
        self.view.setColor(self.START_SPACE_COLOR)

    def _makeFinishSpace(self):
        self.view.setColor(self.FINISH_SPACE_COLOR)

    def _makePathSpace(self):
        self.view.setColor(self.PATH_SPACE_COLOR)
    
    def setStart(self, start = True):
        self.start = start
        self.updateColor()

    def setFinish(self, finish = True):
        self.finish = finish
        self.setState(self.UNDISCOVERED_STATE)

    def setPath(self):
        self.path = True
        self.updateColor()

    def isStart(self):
        return self.start

    def isFinish(self):
        return self.finish

    def _isPath(self):
        return self.path

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
        self.updateColor()

    def draw(self, window):
        self.view.draw(window)

    def undraw(self):
        self.view.undraw()

    def updateColor(self):
        if self.isStart():
            self._makeStartSpace()
        elif self.isFinish():
            self._makeFinishSpace()
        elif self.isWall():
            self._makeWall()
        elif self._isPath():
            self._makePathSpace()
        elif self.state == self.UNDISCOVERED_STATE:
            self._makeUndiscoveredSpace()
        elif self.state == self.DISCOVERED_STATE:
            self._makeDiscoveredSpace()
        elif self.state == self.VISITED_STATE:
            self._makeVisitedSpace()

    def click(self):
        if self.isStart() or self.isFinish():
            return
        if self.isWall():
            self.setState(self.UNDISCOVERED_STATE)
        else:
            self.setState(self.WALL_STATE)

    def setParent(self, node):
        self.parent = node

    def resetState(self):
        if self.isWall():
            return
        self.path = False
        self.parent = None
        self.setState(GridNode.UNDISCOVERED_STATE)