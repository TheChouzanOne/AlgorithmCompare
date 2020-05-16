import graphics as gx

class Instructions:
    def __init__(self, text, position, color = 'black', ):
        self.text = text
        self.position = position
        self.color = color 
        
        self.instructionText = self._getText()

    def draw(self, window):
        self.instructionText.draw(window)

    def setText(self, newText):
        self.text = newText
        self.instructionText.setText("Instructions: %s"%self.text)

    def _getText(self):
        anchor = gx.Point(self.position[0], self.position[1])
        textView = gx.Text(anchor, "Instructions: %s"%self.text)
        textView.setFace('times roman')
        textView.setSize(14)
        textView.setStyle("bold")
        textView.setTextColor(self.color)

        return textView