import os

import pandas as pd
import random
from canvas import canvas

JOKE_FILE = "jokes.csv"

class Jokes:
    def __init__(self, width: int, height: int) -> None:
        self.filePath = os.getcwd()+"/mod_jokes/"+JOKE_FILE
        self.df_jokes = pd.read_csv(self.filePath)
        self.rdIdx = -1
        self.maxIdx = len(self.df_jokes.index)-1
        self.canvas = canvas.Canvas(width, height, margins=10, bgcolor="white")
        self.load_Fonts()

    def load_Fonts(self) -> None:
        os_filePath = os.getcwd()
        self.canvas.addTTF("RobotoLight12", os_filePath+"/fonts/Roboto-Light.ttf", 12)

    def update_RdIdx(self) -> None:
        self.rdIdx = random.randint(0, self.maxIdx)

    def get_random_joke(self) -> str:
        return self.df_jokes.sample(n=1).iloc[0]['Joke']
    
    def get_joke(self, idx: int) -> str:
        if 0 <= idx <= self.maxIdx:
            return self.df_jokes.iloc[idx]['Joke']
        else:
            return "Index out of range"
    
    def increase_counter(self, idx: int) -> None:
        if 0 <= idx <= self.maxIdx:
            self.df_jokes.at[idx, 'Counter'] += 1
    
    def get_counter(self, idx: int) -> int:
        if 0 <= idx <= self.maxIdx:
            return self.df_jokes.at[idx, 'Counter']
        else:
            return -1
        
    def update_jokeFile(self) -> None:
        self.df_jokes.to_csv(self.filePath, index=False)
    
    def write_joke_on_canvas(self, idx: int) -> None:
        joke = self.get_joke(idx)
        replaceStrDict = {
            " — ": "\n-\n",
            " —": "\n-",
            "— ": "-\n"
            } # — 
        self.canvas.addMultilineText(txt=joke, ft="RobotoLight12", fillColor="black", replaceStr=replaceStrDict)
        self.canvas.showImage()
    
    # fr = canvas.Canvas(200, 100, bgcolor="white")

    # filePath = os.getcwd()+"/fonts/Roboto-Light.ttf"
    # fr.addTTF("RobotoLight10", filePath, 10)
    # fr.addMultilineText(10, 10, "Das ist ein Test!", "RobotoLight10", "black")

    # fr.showImage()
    # fr.saveImage("test.png")