from fastapi import FastAPI, Query, HTTPException
from utils import get_weather_data, get_weather_forecast
from ml_model import predict_irrigation
from dotenv import load_dotenv
import csv
import os


# Carrega variáveis de ambiente
load_dotenv()

# Instância principal do FastAPI
app = FastAPI(
    title="Irrigation Forecast API",
    description="API para previsão de irrigação baseada em dados climáticos",
    version="1.0.0"
)

@app.get("/weather")
def get_weather_endpoint(
    city: str = Query(..., min_length=3, description="Nome da cidade"),
    model_type: str = Query("linear", description="Tipo de modelo para previsão de irrigação ('linear', 'tree', 'nn', 'ridge', 'forest')")
):
    """
    Obtém dados climáticos atuais e prevê a necessidade de irrigação.

    Parâmetros:
    - city: Nome da cidade para obter os dados climáticos.
    - model_type: Tipo de modelo para previsão de irrigação ('linear', 'tree', 'nn', 'ridge', 'forest').

    Retorna:
        JSON com dados climáticos atuais (temperatura, umidade, precipitação) e a previsão de irrigação em litros.
    """
    try:
        weather_data = get_weather_data(city)
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        precipitation = weather_data.get("rain", {}).get("1h", 0)

        irrigation = predict_irrigation(temperature, humidity, precipitation, model_type)

        return {
            "city": weather_data["name"],
            "temperature": temperature,
            "humidity": humidity,
            "precipitation": precipitation,
            "predicted_irrigation_liters": round(irrigation, 2)
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados climáticos: {str(e)}")


@app.get("/irrigation-forecast")
def get_irrigation_forecast(
        city: str = Query(..., min_length=3, description="Nome da cidade"),
        model_type: str = Query("linear", description="Tipo de modelo para previsão de irrigação ('linear', 'tree', 'nn', 'ridge', 'forest')")
):
    """
    Obtém a previsão de irrigação com base na previsão climática futura.

    Parâmetros:
    - city: Nome da cidade para obter a previsão climática.
    - model_type: Tipo de modelo para previsão de irrigação ('linear', 'tree', 'nn', 'ridge', 'forest').

    Retorna:
        Lista de previsões de irrigação para os próximos períodos com base em temperatura e umidade.
    """
    try:
        weather_forecast = get_weather_forecast(city)

        if not weather_forecast:
            raise HTTPException(status_code=404, detail="Previsão climática não encontrada.")

        irrigation_forecast = []

        for forecast in weather_forecast:
            temperature = forecast['temp_c']
            humidity = forecast['humidity']
            precipitation = forecast.get("rain", {}).get("1h", 0)
            irrigation = predict_irrigation(temperature, humidity, precipitation, model_type)

            irrigation_forecast.append({
                "timestamp": forecast['time'],
                "temperature": temperature,
                "humidity": humidity,
                "precipitation": precipitation,
                "predicted_irrigation_liters": round(irrigation, 2)
            })

        return irrigation_forecast

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter previsão climática: {str(e)}")


@app.get("/irrigation-history")
def get_irrigation_history():
    """
    Obtém o histórico de previsões de irrigação.

    Retorna:
        Lista do histórico de previsões de irrigação armazenado em um arquivo CSV.
    """
    # Caminho do arquivo CSV
    file_path = "/app/data/log.csv"

    # Garantir que o arquivo seja criado se não existir
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "timestamp",
                        "city",
                        "temperature",
                        "humidity",
                        "precipitation",
                        "predicted_irrigation_liters"
                    ]
                )
                writer.writeheader()

        except PermissionError:
            raise HTTPException(status_code=403, detail="Permissão negada para criar o arquivo.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar o arquivo de histórico: {str(e)}")

    try:
        # Abre e le o arquivo CSV
        with open(file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            history = [row for row in reader]

        # Converte valores para os tipos apropriados
        for entry in history:
            entry['temperature'] = float(entry['temperature'])
            entry['humidity'] = float(entry['humidity'])
            entry['precipitation'] = float(entry['precipitation'])
            entry['predicted_irrigation_liters'] = float(entry['predicted_irrigation_liters'])

        return history
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Histórico de irrigação não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler o histórico de irrigação: {str(e)}")