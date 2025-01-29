from fastapi import APIRouter, Query, HTTPException
import os
import csv
from datetime import datetime
from models.ml_model import predict_irrigation
from utils import get_weather_data, get_weather_forecast

router = APIRouter()

LOG_FILE_PATH = "app/data/irrigation_log.csv"


@router.get("/weather")
def get_weather_endpoint(
    city: str = Query(..., min_length=3, description="Nome da cidade"),
    model_type: str = Query("linear", description="Tipo de modelo para previsão de irrigação ('linear', 'tree', 'nn', 'ridge', 'forest')")
):
    try:
        weather_data = get_weather_data(city)
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        precipitation = weather_data.get("rain", {}).get("1h", 0)
        soil_type = "sandy"

        irrigation = predict_irrigation(temperature, humidity, precipitation, model_type, soil_type)

        return {
            "city": weather_data["name"],
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "precipitation": round(precipitation, 2),
            "soil_type": soil_type,
            "model_type": model_type,
            "predicted_irrigation_liters": round(irrigation, 2),
            "message": "Dados climáticos e previsão de irrigação"
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados climáticos: {str(e)}")


@router.get("/irrigation-forecast")
def get_irrigation_forecast(
        city: str = Query(..., min_length=3, description="Nome da cidade"),
        model_type: str = Query("linear", description="Tipo de modelo para previsão de irrigação ('linear', 'tree', 'nn', 'ridge', 'forest')")
):
    try:
        weather_forecast = get_weather_forecast(city)

        if not weather_forecast:
            raise HTTPException(status_code=404, detail="Previsão climática não encontrada.")

        irrigation_forecast = []

        for forecast in weather_forecast:
            temperature = forecast['temp_c']
            humidity = forecast['humidity']
            precipitation = forecast.get("rain", {}).get("1h", 0)
            soil_type = "sandy"
            irrigation = predict_irrigation(temperature, humidity, precipitation, model_type, soil_type)

            irrigation_forecast.append({
                "timestamp": forecast['time'],
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "precipitation": round(precipitation, 2),
                "soil_type": soil_type,
                "model_type": model_type,
                "predicted_irrigation_liters": round(irrigation, 2)
            })

        return {
            "city": city,
            "forecast": irrigation_forecast,
            "message": "Previsões de irrigação com base no clima"
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter previsão climática: {str(e)}")


@router.get("/irrigation-history")
def get_irrigation_history():
    if not os.path.exists(LOG_FILE_PATH) or os.stat(LOG_FILE_PATH).st_size == 0:
        try:
            with open(LOG_FILE_PATH, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "timestamp",
                        "city",
                        "temperature",
                        "humidity",
                        "precipitation",
                        "predicted_irrigation_liters",
                        "soil_type"
                    ]
                )
                writer.writeheader()

        except PermissionError:
            raise HTTPException(status_code=403, detail="Permissão negada para criar o arquivo.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar o arquivo de histórico: {str(e)}")

    try:
        with open(LOG_FILE_PATH, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            history = [row for row in reader]

        for entry in history:
            entry['temperature'] = float(entry['temperature'])
            entry['humidity'] = float(entry['humidity'])
            entry['precipitation'] = float(entry['precipitation'])
            entry['predicted_irrigation_liters'] = float(entry['predicted_irrigation_liters'])
            entry['soil_type'] = "sandy"

        return {
            "message": "Histórico de irrigação obtido com sucesso",
            "data": history
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Histórico de irrigação não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler o histórico de irrigação: {str(e)}")


@router.get("/optimal-irrigation-time")
def get_optimal_irrigation_time(city: str):
    try:
        weather_data = get_weather_data(city)
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        precipitation = weather_data.get("rain", {}).get("1h", 0)
        soil_type = "sandy"

        # Sugestão baseada na temperatura (evitar irrigar no pico de calor)
        if temperature > 30:
            optimal_time = "early morning or late evening"
        else:
            optimal_time = "morning"

        return {
            "city": weather_data["name"],
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "precipitation": round(precipitation, 2),
            "soil_type": soil_type,
            "suggested_irrigation_time": optimal_time,
            "message": "Horário ideal para irrigação sugerido com base na temperatura"
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados climáticos: {str(e)}")


