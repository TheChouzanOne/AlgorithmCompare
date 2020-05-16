import json
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename

from AlgorithmGrid import AlgorithmGrid

class GridJsonSerializer:
    FILE_EXTENSION = '.json'

    @staticmethod
    def saveToJson(algorithmGrid):
        Tk().withdraw()
        filename = asksaveasfilename(
            defaultextension=GridJsonSerializer.FILE_EXTENSION, 
            filetypes = [
                ('JSON', GridJsonSerializer.FILE_EXTENSION), 
                ('All files', '*')
        ])
        if not filename:
            return

        jsonObject = GridJsonSerializer.convertGridToJson(algorithmGrid)

        with open(filename, 'w') as f:
            f.write(jsonObject)


    @staticmethod
    def loadFile(algorithm):
        Tk().withdraw()
        filename = askopenfilename(
            defaultextension=GridJsonSerializer.FILE_EXTENSION, 
            filetypes = [
                ('JSON', GridJsonSerializer.FILE_EXTENSION), 
                ('All files', '*')
        ])
        with open(filename, 'r') as f:
            content = f.read()
            jsonObject = json.loads(content)

        algorithmGrid = AlgorithmGrid(
            jsonObject['width'],
            jsonObject['height'],
            jsonObject['nodesPerSide'],
            algorithm,
            jsonObject['startPosition'],
            jsonObject['finishPosition']
        )
        
        algorithmGrid.setCellsState(jsonObject['grid'])

        return algorithmGrid
        

    def convertGridToJson(algorithmGrid):
        jsonObject = {
            'width': algorithmGrid.width,
            'height': algorithmGrid.height,
            'nodesPerSide': algorithmGrid.nodesPerSide,
            'startPosition': algorithmGrid.startPosition,
            'finishPosition': algorithmGrid.finishPosition,
            'grid': [
                [ 
                    'W' if cell.isWall() else 'U'    
                for cell in row]
            for row in algorithmGrid.grid]
        }

        return json.dumps(jsonObject)
        
    @staticmethod
    def fromJson(filename):
        pass