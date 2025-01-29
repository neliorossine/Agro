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


def predict_irrigation(temperature: float, humidity: float, precipitation: float, model_type: str,
                       soil_type: str) -> float:
    """
    Prever a necessidade de irrigação com base na temperatura, umidade, precipitação e tipo de solo.

    Parâmetros:
    - temperature: Temperatura atual em °C.
    - humidity: Umidade relativa do ar em %.
    - precipitation: Precipitação em mm.
    - model_type: Tipo de modelo a ser utilizado.
    - soil_type: Tipo de solo (areia, argila, etc.).

    Retorna:
    - Necessidade de irrigação em litros.
    """

    soil_factor = {
        "sandy": 1.2,  # Solos arenosos necessitam de mais irrigação
        "clay": 0.8,  # Solos argilosos retêm mais água
        "loamy": 1.0  # Solos com mistura equilibrada
    }

    # Aplicando o fator de solo
    soil_multiplier = soil_factor.get(soil_type.lower(), 1.0)

    # Previsão básica
    if model_type not in models:
        raise ValueError(f"Modelo '{model_type}' não é suportado.")

    model = models[model_type]
    input_data = np.array([[temperature, humidity]])
    predicted_irrigation = model.predict(input_data)[0]

    # Ajuste para o tipo de solo
    if soil_type == "sandy":
        predicted_irrigation *= 1.2  # Solo arenoso pode precisar de mais irrigação
    elif soil_type == "clay":
        predicted_irrigation *= 0.8  # Solo argiloso pode precisar de menos irrigação

    # Ajuste com base na precipitação
    if precipitation > 0:
        predicted_irrigation -= precipitation * 0.5

    # Ajuste com base no tipo de solo
    predicted_irrigation *= soil_multiplier

    # Garantir que o resultado seja positivo
    return max(predicted_irrigation, 0.0)

