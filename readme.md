# Projeto API Clima

<p align="center"><img src="https://s3.amazonaws.com/1-jacto.com.br/files/banner_image_1680700798649_no-uniport-4530-america-do-sul-sai.webp"></p>

## Descrição
Uma API desenvolvida em FastAPI que fornece dados climáticos de uma cidade utilizando a OpenWeather API e WeatherAPI, realizando então previsões de necessidade de irrigação com base em condições climáticas. Também possui um agendador para tarefas periódicas.

---


## Como rodar o projeto

### 1. Clone este repositório:
```bash
git clone <url-do-repositorio>
cd <diretorio-do-repositorio>
```

### 2. Criar e ativar o ambiente virtual:
Se você preferir usar um ambiente virtual, pode criar um com venv. Aqui estão os passos:

Para Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Para Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Execute o Docker Compose:
Certifique-se de que você tem o Docker e o Docker Compose instalados.

```bash
docker-compose up --build
```

### 4. Acesse a API no navegador:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Endpoints Disponíveis

### `/weather`
Retorna os dados climáticos de uma cidade e uma previsão de irrigação baseada em modelos de IA.

#### Parâmetros de Consulta:
- `city` (string, obrigatório): Nome da cidade.
- `model_type` (string, opcional): Tipo de modelo de previsão de irrigação. Opções: `linear`, `tree`, `nn`, `ridge`, `forest`. Padrão: `linear`.

#### Exemplo de Requisição:
```bash
GET http://localhost:8000/weather?city=Curitiba&model_type=linear
```

#### Exemplo de Resposta:
```json
{
    "city": "Curitiba",
    "temperature": 18.44,
    "humidity": 59,
    "precipitation": 0,
    "predicted_irrigation_liters": 10.5
}
```

### `/irrigation-forecast`
Retorna a previsão de irrigação com base nas condições climáticas futuras de uma cidade, utilizando a WeatherAPI.

#### Parâmetros de Consulta:
- `city` (string, obrigatório): Nome da cidade.

#### Exemplo de Requisição:
```bash
GET http://localhost:8000/irrigation-forecast?city=Curitiba
```

#### Exemplo de Resposta:
```json
{
    "city": "Curitiba",
    "temperature_forecast": [18.5, 31.2, 25.0],
    "humidity_forecast": [60, 58, 55],
    "predicted_irrigation_liters": 15.0
}
```


### `/irrigation-history`
Retorna o histórico de irrigação realizado.

#### Parâmetros de Consulta:
- `city` (string, obrigatório): Nome da cidade.

#### Exemplo de Requisição:
```bash
GET http://localhost:8000/irrigation-history
```

#### Exemplo de Resposta:
```json
[
    {
        "city": "Curitiba",
        "date": "2025-01-23",
        "irrigation_liters": 10.5
    },
    {
        "city": "Curitiba",
        "date": "2025-01-22",
        "irrigation_liters": 12.0
    }
]
```

---

## Agendador de Tarefas
O projeto possui um componente de agendamento que realiza verificações periódicas e pode ser expandido para realizar a coleta de dados automática ou outras tarefas programadas.

- Execução automática no Docker Compose.
- Retorno dos dados são salvos em um arquivo csv.
- Logs das tarefas estão disponíveis no container do scheduler.

---

## Estrutura do Projeto

```
.
├── app/
│   ├── main.py                 # Arquivo principal da API contendo as rotas
│   ├── scheduler.py            # Agendamento de previsões
│   ├── utils.py                # Funções utilitárias
│   ├── requirements.txt        # Dependências do Python
│   ├── Dockerfile              # Configuração para criar a imagem Docker
│   ├── ml_model.py          # Modelos de Machine Learning
│   ├── data
│   │   ├── irrigation_log.csv   # Histórico de irrigação
├── tests/
│   ├── test_routes.py          # Testes das rotas da API
├── .env                        # Variáveis de ambiente

├── docker-compose.yml          # Orquestração dos containers
└── README.md                   # Documentação do projeto
```

---

## Tecnologias Utilizadas
- **Linguagem**: Python 3.10
- **Frameworks**: FastAPI, Schedule
- **Machine Learning**: scikit-learn
- **APIs Externas**: OpenWeather API, WeatherAPI
- **Containerização**: Docker e Docker Compose

---

## Como usar o modelo de aprendizado de máquina
O projeto implementa previsão de irrigação baseada em temperatura e umidade.

#### Exemplo de Previsão:
- Dados de entrada: `temperatura = 32°C`, `umidade = 75%`.
- Saída prevista: `15 litros de água para irrigação`.

Os modelos podem ser expandidos para incluir mais parâmetros ou algoritmos mais sofisticados.

#### Como instalar dependências adicionais para ML (caso necessário):
```bash
pip install -r app/requirements.txt
```


## Testes
O projeto contém testes para as rotas da API, localizados em tests/test_routes.py. Para executar os testes, use:
```bash
python -m unittest tests.test_routes
```
Isso garantirá que as rotas estão funcionando corretamente.


---

## Considerações Finais

Este projeto é modular e preparado para futuras expansões, como:
- **Previsões climáticas a longo prazo**.
- **Otimização de colheitas** com base em condições climáticas.
- **Integração com bancos de dados escaláveis** como MongoDB.

Contribuições e sugestões são bem-vindas!

