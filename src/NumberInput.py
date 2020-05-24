import graphics as gx
from Button import Button

class NumberInput:
    def __init__(self, position, size, clickCallback, defaultNumber = 10, text = ""):
        self.position = position
        self.size = size
        self.text = text
        self.number = defaultNumber

        self._setupNumberEntry()
        self._setupReloadButton(clickCallback)
        self._setupTextLabel()


    def draw(self, window):
        self.reloadButton.draw(window)
        self.numberEntry.draw(window)
        self.textLabel.draw(window)

    def isClicked(self, xClick, yClick):
        return self.reloadButton.isClicked(xClick, yClick)

    def click(self):
        newNumber = self.numberEntry.getText()
        if not newNumber.isnumeric():
            return

        newNumber = int(newNumber)
        if newNumber < 2 or newNumber > 60:
            return
        
        self.number = newNumber
        self.reloadButton.click()

    def _setupReloadButton(self, clickCallback):
        reloadCharacter = '\u27f2'
        reloadColor = 'light blue'
        reloadPosition = (
            self.position[0] + 3 * self.size[0] / 10,
            self.position[1] + self.size[1] / 3
        )
        reloadSize = (
            2 * self.size[0] / 10,
            self.size[1] / 3
        )
        self.reloadButton = Button(reloadCharacter, reloadColor, reloadPosition, reloadSize, clickCallback)

    def _setupNumberEntry(self):
        characterSize = 3
        entryPosition = gx.Point(
            self.position[0] + 2 * self.size[0] / 10,
            self.position[1] + self.size[1] / 2
        )
        self.numberEntry = gx.Entry(entryPosition, characterSize)
        
        self.numberEntry.setFace('times roman')
        self.numberEntry.setText(str(self.number))
        self.numberEntry.setStyle('bold')
        self.numberEntry.setSize(14)

    def _setupTextLabel(self):
        anchor = gx.Point(self.position[0] + self.size[0] / 3, self.position[1] + self.size[1])
        self.textLabel = gx.Text(anchor, self.text)
        self.textLabel.setFace('times roman')
        self.textLabel.setSize(14)
        self.textLabel.setStyle("bold")

    def getNumber(self):
        return self.number

        
