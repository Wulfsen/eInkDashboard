from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Canvas:
    def __init__(self, width: int, height: int, margins: int = 0, bgcolor: str = "white") -> None:
        self.width = width
        self.height = height
        self.margins = margins
        self.img = Image.new('L', (width, height), bgcolor)
        self.draw = ImageDraw.Draw(self.img)
        self.fonts = {}
    
    def addTTF(self, name:str, filePath: str, size: int) ->None:
        self.fonts[name] = ImageFont.truetype(filePath, size)

    def wrap_text_by_pixels(self, text: str, font: ImageFont, max_width: int) -> str:
        lines = []
        words = text.split(' ')
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            # Prüfen, ob die Zeile inklusive des neuen Wortes zu breit ist
            if font.getlength(test_line) <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                
        lines.append(' '.join(current_line))
        return '\n'.join(lines)
    
    def addMultilineText(self, txt: str, ft: str, fillColor: str, replaceStr: dict[str, str] | None = None) -> None:
        tempFont = self.fonts[ft]
        
        txt = self.wrap_text_by_pixels(txt, tempFont, self.width - 2 * self.margins)
        
        if replaceStr:
            for key, value in replaceStr.items():
                txt = txt.replace(key, value)
        position = (self.width/2, self.height/2)
        self.draw.multiline_text(position, txt, font=tempFont, fill=fillColor, align="center", anchor="mm")
    
    def getImage(self) -> Image:
        return self.img
    
    def showImage(self) -> None:
        self.img.show()

    def saveImage(self, name: str) -> None:
        self.img.save(name)
