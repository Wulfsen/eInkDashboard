import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

from canvas import canvas

class FinanceChart:
    def __init__(self, width: int, height: int, canvasConfig:dict, financeConfig:dict) -> None:
        self.canvas = canvas.Canvas(width, height, canvasConfig, margins=10, bgcolor="white")
        self.ticker = financeConfig['ticker']
        self.period = financeConfig['period']
        self.interval = financeConfig['interval']
        self.title = financeConfig['title']
        self.candleMargin = financeConfig['candleMargin']
        self.df_finData: pd.DataFrame = pd.DataFrame()
        
    def fetch_finance_data(self) -> None:
        today = datetime.now()
        start = today - timedelta(days=self.period)
        end = today + timedelta(days=1)  # Include today
        
        df = yf.download(self.ticker, 
                         start=start.strftime('%Y-%m-%d'),
                         end=end.strftime('%Y-%m-%d'),
                        interval=self.interval)
        
        self.df_finData['Open'] = df['Open'].iloc[:, 0].values
        self.df_finData['Close'] = df['Close'].iloc[:, 0].values
        self.df_finData['High'] = df['High'].iloc[:, 0].values
        self.df_finData['Low'] = df['Low'].iloc[:, 0].values
        self.df_finData['Date'] = df.index

    def print_finance_data(self) -> None:
        print(self.df_finData)      

    def save_finance_data(self) -> None:
        self.df_finData.to_csv("finance_data.csv")

    def load_finance_data_from_file(self) -> None:
        self.df_finData = pd.read_csv("finance_data.csv", index_col=0, parse_dates=True)

    def plot_candle_chart(self) -> None:
        margins = self.canvas.margins
        cdlSpace = self.candleMargin
        x : int = margins
        y : int = margins
        diaHeight : int
        diaWidth : int
        scaling : float

        text : str = ""
        
        curVal = self.df_finData['Close'].iloc[-1]
        maxVal = self.df_finData.select_dtypes(include=['number']).max().max()
        minVal = self.df_finData.select_dtypes(include=['number']).min().min()
        deltaVal = maxVal - minVal

        yTop = y + self.canvas.getStrHeight("header")
        yBase = self.canvas.height - margins
        diaHeight = yBase - yTop
        scaling = diaHeight / deltaVal if deltaVal != 0 else 1

        text = self.title + ": " + f"{curVal:,.0f}".replace(',', '.')
        self.canvas.addText(txt=text, ft="header", fillColor="black", position=(x,y))

        minTxt = f"{minVal:,.0f}".replace(',', '.')
        maxTxt = f"{maxVal:,.0f}".replace(',', '.')
        minValTxtWidth = self.canvas.getStrLength(minTxt, "body")
        maxValTxtWidth = self.canvas.getStrLength(maxTxt, "body")
        bodyTxtHeight = self.canvas.getStrHeight("body")

        x = margins
        if minValTxtWidth > maxValTxtWidth:
            x = x + minValTxtWidth - maxValTxtWidth
        self.canvas.addText(txt=maxTxt, ft="body", fillColor="black", position=(x, yTop))

        x = margins
        if maxValTxtWidth > minValTxtWidth:
            x = x + maxValTxtWidth - minValTxtWidth
        self.canvas.addText(txt=minTxt, ft="body", fillColor="black", position=(x, yBase - bodyTxtHeight))
        
        x = margins + max(minValTxtWidth, maxValTxtWidth) + cdlSpace
        self.canvas.draw.line([(x, yTop), (x, yBase)], fill="black", width=1)
        
        diaWidth = self.canvas.width - x - margins
        candleWidth = int(diaWidth / len(self.df_finData) - cdlSpace / 2)        
        
        i=0
        x0 = x + cdlSpace
        while i < len(self.df_finData):
            open = self.df_finData['Open'].iloc[i]
            close = self.df_finData['Close'].iloc[i]
            high = self.df_finData['High'].iloc[i]
            low = self.df_finData['Low'].iloc[i]

            x = x0 + i * (candleWidth + cdlSpace)
            x1 = x + candleWidth
            
            yOpen = yBase - int((open - minVal) * scaling)
            yClose = yBase - int((close - minVal) * scaling)
            yHigh = yBase - int((high - minVal) * scaling)
            yLow = yBase - int((low - minVal) * scaling)

            if close >= open:
                fillColor = "white"
                self.canvas.draw.rectangle([(x, yClose), (x1, yOpen)], fill=fillColor, outline="black")
                self.canvas.draw.line([(x + candleWidth // 2, yHigh), (x + candleWidth // 2, yClose)], fill="black", width=1)
                self.canvas.draw.line([(x + candleWidth // 2, yOpen), (x + candleWidth // 2, yLow)], fill="black", width=1)
            else:
                fillColor = "black"
                self.canvas.draw.rectangle([(x, yOpen), (x1, yClose)], fill=fillColor, outline="black")
                self.canvas.draw.line([(x + candleWidth // 2, yHigh), (x + candleWidth // 2, yOpen)], fill="black", width=1)
                self.canvas.draw.line([(x + candleWidth // 2, yClose), (x + candleWidth // 2, yLow)], fill="black", width=1)
        
            i = i + 1
        self.canvas.showImage()




        
