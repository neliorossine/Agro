from fastapi import FastAPI
from irrigation import router as irrigation_router
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Instância principal do FastAPI
app = FastAPI(
    title="Irrigation Forecast API",
    description="API para previsão e otimização de irrigação baseada em dados climáticos",
    version="1.0.0"
)

# Registra as rotas do módulo de irrigação
app.include_router(irrigation_router)
