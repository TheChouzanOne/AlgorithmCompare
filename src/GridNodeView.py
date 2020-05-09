import graphics as gx

class GridNodeView:    
    def __init__(self, row, column, color, config):
        self.config = config
        
        position = self._getCellPosition(row, column)
        Point1 = gx.Point(position['x1'], position['y1'])
        Point2 = gx.Point(position['x2'], position['y2'])
        self.Rectangle = gx.Rectangle(Point1, Point2)
        self.setColor(color)

    def setColor(self, color):
        self.Rectangle.setFill(color)

    def draw(self, window):
        # Not sure if I have to redraw for color to update
        self.Rectangle.draw(window)

    def _getCellPosition(self, row, column):
        return {
            'x1': self.config['algorithmColumns']['xOffsetUL'] + \
                    self.config['algorithmNodes']['offset'] + \
                    column * self.config['algorithmNodes']['size'],
            'y1': self.config['algorithmColumns']['yOffsetUL'] + \
                    self.config['algorithmNodes']['offset'] + \
                    row * self.config['algorithmNodes']['size'],
            'x2': self.config['algorithmColumns']['xOffsetUL'] + \
                    self.config['algorithmNodes']['offset'] + \
                    self.config['algorithmNodes']['nodeSize'] + \
                    column * self.config['algorithmNodes']['size'],
            'y2': self.config['algorithmColumns']['yOffsetUL'] + \
                    self.config['algorithmNodes']['offset'] + \
                    self.config['algorithmNodes']['nodeSize'] + \
                    row * self.config['algorithmNodes']['size']
        }