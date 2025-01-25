import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather_data(city: str):
    """
    Obtém dados climáticos atuais da cidade usando a API OpenWeather.

    Parâmetros:
    - city: Nome da cidade a ser consultada.

    Retorna:
    - Dados climáticos atuais (temperatura, umidade, precipitação).
    """
    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("BASE_URL")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erro ao obter dados climáticos da OpenWeather")

def get_weather_forecast(city: str):
    """
    Obtém a previsão climática para os próximos períodos (3 horas) usando a WeatherAPI.

    Parâmetros:
    - city: Nome da cidade para obter a previsão.

    Retorna:
    - Previsão climática para as próximas horas.
    """
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_API_URL = os.getenv("WEATHER_API_URL")

    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "days": 1,
        "hour": 3,
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        return response.json()['forecast']['forecastday'][0]['hour']
    else:
        raise Exception("Erro ao obter previsão climática da WeatherAPI")
