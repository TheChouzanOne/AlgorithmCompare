import graphics as gx

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

    def __init__(self, row, column, config):
        self.state = self.UNDISCOVERED_STATE
        self.view = GridNodeView(row, column, self.UNDISCOVERED_SPACE_COLOR, config)

    def _isWall(self):
        return self.state == self.WALL_STATE

    def _makeWall(self):
        self.view.setColor(self.WALL_SPACE_COLOR)

    def _makeUndiscoveredSpace(self):
        self.view.setColor(self.UNDISCOVERED_SPACE_COLOR)

    def _makeDiscoveredSpace(self):
        self.view.setColor(self.DISCOVERED_SPACE_COLOR)

    def _makeVisitedSpace(self):
        self.view.setColor(self.VISITED_SPACE_COLOR)

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
        self.updateColor()

    def draw(self, window):
        self.view.draw(window)

    def updateColor(self):
        if self._isWall():
            self._makeWall()
        elif self.state == self.UNDISCOVERED_STATE:
            self._makeUndiscoveredSpace()
        elif self.state == self.DISCOVERED_STATE:
            self._makeDiscoveredSpace()
        elif self.state == self.VISITED_STATE:
            self._makeVisitedSpace()

    def click(self):
        if self._isWall():
            self.setState(self.UNDISCOVERED_STATE)
        else:
            self.setState(self.WALL_STATE)