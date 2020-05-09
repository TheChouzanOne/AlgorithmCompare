import graphics as gx

class AlgorithmGridView:
    def __init__(self, width, height, nodesPerSide, config):
        self.config = config
        self.background = self._getAlgorithmGridBackground()

    def draw(self, window):
        self.background.draw(window)

    def setBackgroundColor(self, color):
        self.background.setFill(color)

    def _getAlgorithmGridBackground(self):
        P1 = gx.Point(
            self.config['algorithmColumns']['xOffsetUL'],
            self.config['algorithmColumns']['yOffsetUL'],
        )
        P2 = gx.Point(
            self.config['algorithmColumns']['xOffsetLR'],
            self.config['algorithmColumns']['yOffsetLR'],
        )

        background = gx.Rectangle(P1, P2)
        background.setFill('black')

        return background