import os
import sys

from PIL import Image
from PIL import ImageDraw

class Canvas:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.img = Image.new('L', (width, height), 125)

    def getImage(self) -> Image:
        return self.img
    
    def showImage(self) -> None:
        self.img.show()
        input("Press ENTER to exit")

    def saveImage(self) -> None:
        self.img.save("test.png")