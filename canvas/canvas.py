import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Canvas:
    def __init__(self, width: int, height: int, fontConfig: dict, margins: int = 0, bgcolor: str = "white") -> None:
        self.width = width
        self.height = height
        self.margins = margins
        self.img = Image.new('L', (width, height), bgcolor)
        self.draw = ImageDraw.Draw(self.img)
        self.fonts = {}
        self.load_Fonts(fontConfig)
    
    def addTTF(self, name:str, filePath: str, size: int) ->None:
        self.fonts[name] = ImageFont.truetype(filePath, size)

    def load_Fonts(self, fontConfig: dict) -> None:
        path = os.getcwd() + "/fonts/"
        
        self.addTTF(name="header", filePath=path + fontConfig['font_header'], size=int(fontConfig['size_header']))
        self.addTTF(name="subheader", filePath=path + fontConfig['font_subheader'], size=int(fontConfig['size_subheader']))
        self.addTTF(name="subheader_bold", filePath=path + fontConfig['font_subheader_bold'], size=int(fontConfig['size_subheader']))
        self.addTTF(name="body", filePath=path + fontConfig['font_body'], size=int(fontConfig['size_body']))
    
    def getStrLength(self, text: str, fontName: str) -> int:
        font = self.fonts[fontName]
        return font.getlength(text)
    
    def getStrHeight(self, fontName: str) -> int:
        font = self.fonts[fontName]
        ascent, descent = font.getmetrics()
        return ascent + descent

       
    def wrap_text_by_pixels(self, text: str, font: ImageFont, max_width: int) -> str:
        paragraphs = text.split('\n')
        final_lines = []

        for paragraph in paragraphs:
            words = paragraph.split(' ')
            current_line = []

            for word in words:
                test_line = ' '.join(current_line + [word])
                # Prüfen, ob die Zeile inklusive des neuen Wortes zu breit ist
                if font.getlength(test_line) <= max_width:
                    current_line.append(word)
                else:
                    final_lines.append(' '.join(current_line))
                    current_line = [word]
            
            final_lines.append(' '.join(current_line))
        
        return '\n'.join(final_lines)
    
    def addText(self, txt: str, ft: str, fillColor: str, position: tuple[int, int]) -> None:
        font = self.fonts[ft]
        self.draw.text(position, txt, font=font, fill=fillColor)
    
    def addText_Tester(self, txt: str, ft: str, fillColor: str, position: tuple[int, int]) -> None:
        font = self.fonts[ft]
        self.draw.text(position, txt, font=font, fill=fillColor)
        ascent, descent = font.getmetrics()
        (width, height), (offset_x, offset_y) = font.font.getsize(txt)
        print("width: " + str(width) + " height: " + str(height) + " offset_x: " + str(offset_x) + " offset_y: " + str(offset_y))
        x0 = position[0]
        y0 = position[1] +  offset_y
        x1 = position[0] + font.getlength(txt)
        y1 = position[1] + ascent + descent
        print("x0: " + str(x0) + " y0: " + str(y0) + " x1: " + str(x1) + " y1: " + str(y1))
        self.draw.rectangle([(x0, y0), (x1, y1)], outline="red")
        #self.draw.rectangle([(0, offset_y), (font.getmask(txt).getbbox()[2], ascent + descent)], fill=(202, 229, 134))
        #bbox = self.draw.textbbox(position, txt, font=font)
        #self.draw.rectangle(bbox, outline="red")
        #print(bbox)

    def addMultilineText(self, txt: str, ft: str, fillColor: str, position: tuple[int, int], width: int, replaceStr: dict[str, str] | None = None, align: str = "center", anc: str = "la") -> None:
        tempFont = self.fonts[ft]

        txt = self.wrap_text_by_pixels(txt, tempFont, width)
        
        if replaceStr:
            for key, value in replaceStr.items():
                txt = txt.replace(key, value)

        self.draw.multiline_text(position, txt, font=tempFont, fill=fillColor, align=align, anchor=anc)
    
    def getImage(self) -> Image:
        return self.img
    
    def showImage(self) -> None:
        self.img.show()

    def saveImage(self, name: str) -> None:
        self.img.save(name)
