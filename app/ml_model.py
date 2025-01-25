import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor

# Dados fictícios para treinamento do modelo
X = np.array([
    [28, 75],  # Temperatura, Umidade
    [30, 80],
    [32, 70],
    [27, 65],
    [34, 85],
    [29, 72],
    [33, 78],
    [31, 68],
    [26, 60],
    [30, 77],
])

y = np.array([12, 14, 16, 10, 18, 13, 17, 15, 9, 14])  # Necessidade de irrigação em litros

# Inicializa os modelos
models = {
    "linear": LinearRegression(),
    "tree": DecisionTreeRegressor(),
    "nn": MLPRegressor(hidden_layer_sizes=(10,), max_iter=1000, random_state=42),
    "ridge": Ridge(alpha=1.0),
    "forest": RandomForestRegressor(n_estimators=100, random_state=42),
}

# Treinamento dos modelos
for model in models.values():
    model.fit(X, y)

def predict_irrigation(temperature: float, humidity: float, precipitation: float, model_type: str) -> float:
    """
    Prever a necessidade de irrigação com base na temperatura, umidade e precipitação.

    Parâmetros:
    - temperature: Temperatura atual em °C.
    - humidity: Umidade relativa do ar em %.
    - precipitation: Precipitação em mm (valor para ajuste).
    - model_type: Tipo de modelo a ser utilizado ('linear', 'tree', 'nn', 'ridge', 'random_forest').

    Retorna:
    - Necessidade de irrigação em litros.
    """

    if model_type not in models:
        raise ValueError(f"Modelo '{model_type}' não é suportado. Escolha entre {list(models.keys())}.")

    model = models[model_type]
    input_data = np.array([[temperature, humidity]])
    predicted_irrigation = model.predict(input_data)[0]

    # Ajusta com base na precipitação
    if precipitation > 0:
        predicted_irrigation -= precipitation * 0.5

    # Garantir que o resultado seja positivo
    return max(predicted_irrigation, 0.0)
