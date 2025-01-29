from utils import get_weather_data, get_weather_forecast
from models.ml_model import predict_irrigation
import schedule
import time
from datetime import datetime
import logging
import csv
import os

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Caminho do arquivo CSV
FILE_PATH = "/app/data/log.csv"

def save_to_csv(data):
    """
    Salva os dados em um arquivo CSV.

    Args:
        data (list): Lista contendo os dados a serem salvos no arquivo CSV.
    """
    file_exists = os.path.exists(FILE_PATH)

    with open(FILE_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "city", "temperature", "humidity", "precipitation", "predicted_irrigation_liters"])
        writer.writerow(data)

def adjust_schedule_based_on_weather():
    """
    Ajusta a frequência de execução do agendador com base na previsão do tempo.

    Returns:
        int: Frequência em segundos para a próxima execução do job.
    """
    city = "Curitiba"
    try:
        weather_forecast = get_weather_forecast(city)
        upcoming_precipitation = weather_forecast[0].get('rain', {}).get('1h', 0)

        # Ajuste da frequência com base na precipitação
        if upcoming_precipitation > 0:
            return 3600  # Aguarda uma hora se houver previsão de chuva
        else:
            return 30  # Frequência mais curta sem previsão de chuva
    except Exception as e:
        logger.error(f"Erro ao ajustar a frequência: {str(e)}")
        return 60  # Frequência padrão em caso de erro


def job():
    """
    Função principal do job que obtém dados climáticos e prevê a necessidade de irrigação.

    Obtém dados de temperatura, umidade e precipitação de uma cidade específica,
    calcula a necessidade de irrigação e salva os resultados em um arquivo CSV.
    """
    city = "Curitiba"
    model_type = "linear"
    soil_type = "sandy"

    try:
        weather_data = get_weather_data(city)
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        precipitation = weather_data.get("rain", {}).get("1h", 0)

        # Passando o 'soil_type' para a função de previsão
        irrigation = predict_irrigation(temperature, humidity, precipitation, model_type, soil_type)

        data = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            weather_data["name"],
            temperature,
            humidity,
            precipitation,
            round(irrigation, 2)
        ]

        save_to_csv(data)
        logger.info(f"Dados salvos: {data}")
    except Exception as e:
        logger.error(f"Erro ao executar o job: {str(e)}")


def run_schedule():
    """
    Executa o agendador para rodar tarefas em intervalos definidos.

    Ajusta a frequência de execução dinamicamente com base na previsão do tempo.
    """
    frequency = adjust_schedule_based_on_weather()
    schedule.every(frequency).seconds.do(job)

    while True:
        try:
            current_frequency = adjust_schedule_based_on_weather()
            if current_frequency != frequency:
                schedule.clear()
                frequency = current_frequency
                schedule.every(frequency).seconds.do(job)
                logger.info(f"Frequência ajustada para {frequency} segundos")

            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logger.error(f"Erro no agendador: {str(e)}")
            time.sleep(10)

# Iniciar o agendador
if __name__ == "__main__":
    try:
        run_schedule()
    except KeyboardInterrupt:
        logger.info("Scheduler interrompido.")
