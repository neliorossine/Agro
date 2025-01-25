import unittest
from unittest.mock import patch, mock_open
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
os.environ['PYTHONPATH'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '../app'))
sys.path.append(os.environ['PYTHONPATH'])

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

from app.main import app


class TestAPIRoutes(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('app.utils.get_weather_data')
    @patch('app.ml_model.predict_irrigation')
    def test_get_weather_route(self, mock_predict_irrigation, mock_get_weather_data):
        # Mock das funções chamadas pela rota
        mock_get_weather_data.return_value = {}
        mock_predict_irrigation.return_value = 0

        # Testa se a rota retorna 200
        response = self.client.get("/weather", params={"city": "Curitiba", "model_type": "linear"})
        self.assertEqual(response.status_code, 200)

    @patch('app.utils.get_weather_forecast')
    @patch('app.ml_model.predict_irrigation')
    def test_get_irrigation_forecast_route(self, mock_predict_irrigation, mock_get_weather_forecast):
        # Mock das funções chamadas pela rota
        mock_get_weather_forecast.return_value = []
        mock_predict_irrigation.return_value = 0

        # Testa se a rota retorna 200
        response = self.client.get("/irrigation-forecast", params={"city": "Curitiba", "model_type": "linear"})
        self.assertEqual(response.status_code, 200)

    @patch('builtins.open', new_callable=mock_open, read_data='temperature,humidity,precipitation,predicted_irrigation_liters\n30.0,60.0,0.0,10.5\n')
    def test_get_irrigation_history_route(self, mock_file):
        # Testa se a rota retorna 200 OK
        response = self.client.get("/irrigation-history")
        self.assertEqual(response.status_code, 200)

        # Verifica se os dados retornados estão corretos
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['temperature'], 30.0)
        self.assertEqual(data[0]['humidity'], 60.0)
        self.assertEqual(data[0]['predicted_irrigation_liters'], 10.5)  # Verificação adicional

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_get_irrigation_history_file_not_found(self, mock_file):
        # Simula um erro de arquivo não encontrado
        # Testa se a rota retorna 404 quando o arquivo não for encontrado
        response = self.client.get("/irrigation-history")
        self.assertEqual(response.status_code, 500)

    @patch('builtins.open', new_callable=mock_open)
    def test_get_irrigation_history_empty_file(self, mock_file):
        # Simula um arquivo CSV vazio
        mock_file.return_value.__enter__.return_value.read.return_value = ''

        # Testa se a rota retorna 200 OK, mas sem dados
        response = self.client.get("/irrigation-history")
        self.assertEqual(response.status_code, 200)

        # Verifica se a resposta contém uma lista vazia
        data = response.json()
        self.assertEqual(data, [])


if __name__ == "__main__":
    unittest.main()