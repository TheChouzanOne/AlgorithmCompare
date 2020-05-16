import graphics as gx

class AlgorithmGridView:
    def __init__(self, width, height, nodesPerSide, config):
        self.config = config
        self.background = self._getAlgorithmGridBackground()
        self.titleLabel = self._getTitleLabel()

    def draw(self, window):
        self.titleLabel.draw(window)
        self.background.draw(window)

    def undraw(self):
        self.titleLabel.undraw()
        self.background.undraw()

    def setBackgroundColor(self, color):
        self.background.setFill(color)

    def _getTitleLabel(self):
        anchorPoint = gx.Point(
            self.config['title']['x'],
            self.config['title']['y'],
        )
        title = gx.Text(anchorPoint, self.config['algorithm'])
        title.setFace('times roman')
        title.setSize(18)
        title.setStyle('bold')

        return title

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