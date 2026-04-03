import os
import requests
import json
import pandas as pd
from PIL import ImageFont
from datetime import datetime, timezone 
from canvas import canvas


class Weather:
    def __init__(self, width: int, height: int, canvasConfig:dict, owmConfig: dict[str, str]) -> None:
        self.canvas = canvas.Canvas(width, height, canvasConfig, margins=10, bgcolor="grey")
        self.owm_api_key = owmConfig['api_key']
        self.lat = owmConfig['latitude']
        self.long = owmConfig['longitude']
        self.units = owmConfig['units']
        self.weather_actual: dict = {}
        self.weather_forecast: dict = {}
        self.weather_forecast_df_complete: pd.DataFrame = pd.DataFrame()
        self.weather_forecast_df_summary: pd.DataFrame = pd.DataFrame()
        self.iconMap: dict = {}
        self.load_customFonts()
    
    def load_customFonts(self) -> None:
        os_filePath = os.getcwd()
        self.canvas.addTTF("icons", os_filePath+"/fonts/weathericons-regular-webfont.ttf", 48)
        
        with open(os_filePath+'/fonts/WeatherIconMapping.json', 'r', encoding='utf-8') as f:
            tmp = json.load(f)
            self.iconMap = tmp['OWMtoWeatherIcon']

    def fetch_weather_forecast(self) -> None:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        response = requests.get(url, params={
            "lat": self.lat,
            "lon": self.long,
            "units": self.units,
            "appid": self.owm_api_key
        })

        if response.status_code == 200:
            self.weather_forecast = response.json()
        else:
            print(f"Error fetching weather data: {response.status_code}")

    def fetch_weather_actual(self) -> None:
        url = "https://api.openweathermap.org/data/2.5/weather"
        response = requests.get(url, params={
            "lat": self.lat,
            "lon": self.long,
            "units": self.units,
            "appid": self.owm_api_key
        })

        if response.status_code == 200:
            self.weather_actual = response.json()
        else:
            print(f"Error fetching weather data: {response.status_code}")
    
    def save_weather_data(self) -> None:
        with open('weather_forecast.json', 'w', encoding='utf-8') as f:
            json.dump(self.weather_forecast, f, ensure_ascii=False, indent=4)
        with open('weather_actual.json', 'w', encoding='utf-8') as f:
            json.dump(self.weather_actual, f, ensure_ascii=False, indent=4)

    def load_weather_data_from_files(self) -> None:
        with open('weather_forecast.json', 'r', encoding='utf-8') as f:
            self.weather_forecast = json.load(f)
        with open('weather_actual.json', 'r', encoding='utf-8') as f:
            self.weather_actual = json.load(f)

    def convert_forecast_to_dataframe(self) -> None:
        self.weather_forecast_df_complete.iloc[:0]
        if not self.weather_forecast:
            print("No weather forecast data available.")
            return None
        
        unix_ts : int
        dt : datetime
        i = 0
        row_list = []
        while i < len(self.weather_forecast['list']):
            unix_ts = self.weather_forecast['list'][i]['dt']
            dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
            dictItems = {}
            dictItems = {
                "dt": dt,
                "day": dt.day,
                "day_of_week": dt.strftime("%a"),
                "temp": self.weather_forecast['list'][i]['main']['temp'],
                "id": self.weather_forecast['list'][i]['weather'][0]['id'],
                "icon": self.weather_forecast['list'][i]['weather'][0]['icon'],
                "speed": self.weather_forecast['list'][i]['wind']['speed'],
                "deg": self.weather_forecast['list'][i]['wind']['deg'],
                "gust": self.weather_forecast['list'][i]['wind']['gust']
            }
            row_list.append(dictItems)
            i += 1
        self.weather_forecast_df_complete = pd.DataFrame(row_list)
        self.weather_forecast_df_complete = self.weather_forecast_df_complete.sort_values(by='dt', ascending=True).reset_index(drop=True)
        #print(self.weather_forecast_df_complete)
    
    def summarize_weather_forecast(self) -> None:
        self.weather_forecast_df_summary.iloc[:0]

        self.weather_forecast_df_summary = self.weather_forecast_df_complete.groupby('day').agg({
            'id': lambda x: x.mode().iloc[0],
            'icon': lambda x: x.mode().iloc[0],
            'speed': 'mean',
            'deg': 'mean',
            'gust': 'max',
            "day_of_week": lambda x: x.mode().iloc[0]
        }).reset_index()
        
        i : int
        min_temp_list = []
        max_temp_list = []
        i = 0

        while i < len(self.weather_forecast_df_summary):
            day = self.weather_forecast_df_summary.loc[i, 'day']
            min_temp = self.weather_forecast_df_complete[self.weather_forecast_df_complete['day'] == day]['temp'].min()
            max_temp = self.weather_forecast_df_complete[self.weather_forecast_df_complete['day'] == day]['temp'].max()
            min_temp_list.append(min_temp)
            max_temp_list.append(max_temp)
            i += 1
        self.weather_forecast_df_summary['min_temp'] = min_temp_list
        self.weather_forecast_df_summary['max_temp'] = max_temp_list
        #print(self.weather_forecast_df_summary)

    def degreesToTextDesc(self, deg):
        if deg > 337.5: return "Nord"
        if deg > 292.5: return "Nordwest"
        if deg > 247.5: return "West"
        if deg > 202.5: return "Suedwest"
        if deg > 157.5: return "Sued"
        if deg > 122.5: return "Suedost"
        if deg >  67.5: return "Ost"
        if deg >  22.5: return "Nordost"
        return "Nord"
    
    def degreesToTextDescShort(self, deg):
        if deg > 337.5: return "N"
        if deg > 292.5: return "NW"
        if deg > 247.5: return "W"
        if deg > 202.5: return "SW"
        if deg > 157.5: return "S"
        if deg > 122.5: return "SO"
        if deg >  67.5: return "O"
        if deg >  22.5: return "NO"
        return "N"
    
    def print_weather_forecast(self, nDays: int) -> None:
        margins : int = self.canvas.margins
        secWidth : int = (self.canvas.width - 2 * margins) / nDays
        x : int = margins
        y : int = margins
        i : int = 0
        text : str = ""
        
        if nDays > len(self.weather_forecast_df_summary):
            nDays = len(self.weather_forecast_df_summary)

        text = "Wetter"
        self.canvas.addText(txt=text, ft="header", fillColor="black", position=(x, y))
        
        unix_ts = self.weather_actual['dt']
        dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
        text = "Aktualisiert: " + dt.strftime("%d.%m.%Y %H:%M")
        self.canvas.addText(txt=text, ft="body", fillColor="black", position=(
            self.canvas.width - margins - self.canvas.getStrLength(text, "body"), y))

        y = y + self.canvas.getStrHeight("header")

        text = "Aktuell: "
        self.canvas.addText(txt=text, ft="subheader_bold", fillColor="black", position=(x, y))

        x = x + self.canvas.getStrLength(text, "subheader_bold")
        text = (str(round(self.weather_actual['main']['temp'])) + 
                "°C | Wind: " + str(round(self.weather_actual['wind']['speed']*3.6)) +
                " (" + str(round(self.weather_actual['wind']['gust']*3.6)) + ") km/h " +
                self.degreesToTextDesc(self.weather_actual['wind']['deg']))
        self.canvas.addText(txt=text, ft="subheader", fillColor="black", position=(x, y))
        
        y = y + self.canvas.getStrHeight("subheader") + margins / 2

        i = 0
        while i < nDays:
            text = self.weather_forecast_df_summary.loc[i, 'day_of_week']
            tmpWidth = self.canvas.getStrLength(text, "subheader_bold")
            x = margins + secWidth * i + (secWidth - tmpWidth) / 2
            self.canvas.addText(txt=text, ft="subheader_bold", fillColor="black", position=(x, y))
            i = i + 1

        y = y + self.canvas.getStrHeight("subheader_bold")

        i = 0
        while i < nDays:
            id = self.weather_forecast_df_summary.loc[i, 'id']
            text = self.iconMap.get(str(id))
            tmpWidth = self.canvas.getStrLength(text, "icons")
            x = margins + secWidth * i + (secWidth - tmpWidth) / 2
            self.canvas.addText(txt=text, ft="icons", fillColor="black", position=(x, y))
            i = i + 1

        y = y + self.canvas.getStrHeight("icons")

        i = 0
        while i < nDays:
            min_temp = self.weather_forecast_df_summary.loc[i, 'min_temp']
            max_temp = self.weather_forecast_df_summary.loc[i, 'max_temp']
            speed = self.weather_forecast_df_summary.loc[i, 'speed']
            deg = self.weather_forecast_df_summary.loc[i, 'deg']
            gust = self.weather_forecast_df_summary.loc[i, 'gust']
            
            text = (str(round(min_temp)) + "°C / " + str(round(max_temp)) + "°C\n" +
                    str(round(speed*3.6)) + " (" + str(round(gust*3.6)) + ") km/h " +
                    self.degreesToTextDescShort(deg))
            
            tmpWidth = self.canvas.getStrLength(text, "body")
            x = margins + secWidth * i + (secWidth) / 2
            
            self.canvas.addMultilineText(txt=text, ft="body", fillColor="black", position=(x, y), width=secWidth, anc="ma")

            i = i + 1


        #self.canvas.addText(txt=text, ft="icons", fillColor="black", position=(self.canvas.width/2, self.canvas.height/2))
        self.canvas.showImage()