import os
import json
import locale
from mod_jokes import jokes
from mod_weather import weather
from mod_financeChart import financeChart

EDP_WIDTH: int = 800
EDP_HEIGHT: int = 480

#Load config data
with open(os.getcwd() + '/config.json') as config_file:
    configData = json.load(config_file)

weatherConfig = configData['weather']
canvasConfig = configData['canvas']
financeConfig = configData['finance']

def main()->None:

    try:
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    except:
        print("Locale konnte nicht gesetzt werden. Wochentage werden möglicherweise nicht korrekt angezeigt.")
    
    #j = jokes.Jokes(EDP_WIDTH, EDP_HEIGHT)
    #j.write_joke_on_canvas(0)#

    #w = weather.Weather(EDP_WIDTH, int(EDP_HEIGHT*0.4), canvasConfig, weatherConfig)
    #w.load_weather_data_from_files()
    #w.convert_forecast_to_dataframe()
    #w.summarize_weather_forecast()
    #w.print_weather_forecast(6)

    f = financeChart.FinanceChart(int(EDP_WIDTH / 2), int(EDP_HEIGHT*0.6), canvasConfig, financeConfig)
    #f.fetch_finance_data()
    f.load_finance_data_from_file()
    f.print_finance_data()
    #f.save_finance_data()
    f.plot_candle_chart()

if __name__ == '__main__':
    main()