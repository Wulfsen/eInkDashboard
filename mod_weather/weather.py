import os

from canvas import canvas

class Weather:
    def __init__(self, width: int, height: int) -> None:
        self.canvas = canvas.Canvas(width, height, margins=10, bgcolor="white")

        self.load_Fonts()
    
    def load_Fonts(self) -> None:
        os_filePath = os.getcwd()
        self.canvas.addTTF("RobotoLight12", os_filePath+"/fonts/Roboto-Light.ttf", 12)