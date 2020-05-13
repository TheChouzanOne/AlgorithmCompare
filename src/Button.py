import graphics as gx

class Button:
    def __init__(self, text, color, position, size, clickCallback):
        self.text = text
        self.color = color
        self.position = position
        self.size = size
        self.clickCallback = clickCallback

        self.button = self._getRectangle()
        self.textView = self._getText()

    def draw(self, window):
        self.button.draw(window)
        self.textView.draw(window)

    def isClicked(self, xClick, yClick):
        if xClick >= self.position[0] and xClick <= self.position[0] + self.size[0] and \
            yClick >= self.position[1] and yClick <= self.position[1] + self.size[1]:
            return True
        return False

    def click(self):
        self.clickCallback()

    def _getRectangle(self):
        P1 = gx.Point( self.position[0], self.position[1] )
        P2 = gx.Point( self.position[0] + self.size[0], self.position[1] + self.size[1])
        button = gx.Rectangle(P1, P2)
        button.setFill(self.color)

        return button

    def _getText(self):
        anchor = gx.Point(self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)
        textView = gx.Text(anchor, self.text)
        textView.setFace('times roman')
        textView.setSize(14)
        textView.setStyle("bold")

        return textView

        
