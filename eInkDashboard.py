import os
import json
import locale
from mod_jokes import jokes
from mod_weather import weather

EDP_WIDTH: int = 800
EDP_HEIGHT: int = 480

#Load config data
with open(os.getcwd() + '/config.json') as config_file:
    configData = json.load(config_file)

weatherConfig = configData['weather']
fontConfig = configData['fonts']

def main()->None:

    try:
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    except:
        print("Locale konnte nicht gesetzt werden. Wochentage werden möglicherweise nicht korrekt angezeigt.")
    
    #j = jokes.Jokes(EDP_WIDTH, EDP_HEIGHT)
    #j.write_joke_on_canvas(0)#

    w = weather.Weather(EDP_WIDTH, int(EDP_HEIGHT*0.4), fontConfig, weatherConfig)
    w.load_weather_data_from_files()
    w.convert_forecast_to_dataframe()
    w.summarize_weather_forecast()
    w.print_weather_forecast(5)

if __name__ == '__main__':
    main()