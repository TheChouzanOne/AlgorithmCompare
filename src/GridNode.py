import graphics as gx

class GridNode:
    
    WALL_STATE = 'wall'
    UNDISCOVERED_STATE = 'undiscovered'
    DISCOVERED_STATE = 'discovered'
    VISITED_STATE = 'visited'

    WALL_SPACE_COLOR = 'black'
    UNDISCOVERED_SPACE_COLOR = 'lightgray'
    DISCOVERED_SPACE_COLOR = 'gray'
    VISITED_SPACE_COLOR = 'blue'

    def __init__(self):
        self.state = self.UNDISCOVERED_STATE
        self.color = self.UNDISCOVERED_SPACE_COLOR

    def __str__(self):
        colorMap = {
            self.WALL_SPACE_COLOR: 'W',
            self.UNDISCOVERED_SPACE_COLOR: 'U',
            self.DISCOVERED_SPACE_COLOR: 'D',
            self.VISITED_SPACE_COLOR: 'V'
        }
        return colorMap[self.color]

    def isWall(self):
        return self.state == self.WALL_STATE

    def makeWall(self):
        self.color = self.WALL_SPACE_COLOR

    def makeUndiscoveredSpace(self):
        self.color = self.UNDISCOVERED_SPACE_COLOR

    def makeDiscoveredSpace(self):
        self.color = self.DISCOVERED_SPACE_COLOR

    def makeVisitedSpace(self):
        self.color = self.VISITED_SPACE_COLOR

    def getColor(self):
        return self.color

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
        self.updateColor()

    def updateColor(self):
        if self.isWall():
            self.makeWall()
        elif self.state == self.UNDISCOVERED_STATE:
            self.makeUndiscoveredSpace()
        elif self.state == self.DISCOVERED_STATE:
            self.makeDiscoveredSpace()
        elif self.state == self.VISITED_STATE:
            self.makeVisitedSpace()

    def click(self):
        if self.isWall():
            self.setState(self.UNDISCOVERED_STATE)
        else:
            self.setState(self.WALL_STATE)