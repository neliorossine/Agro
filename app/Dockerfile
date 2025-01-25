FROM python:3.9-slim AS build

WORKDIR /app

# Instalar dependências
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta 8000 para o FastAPI
EXPOSE 8000

# Rodar o FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

