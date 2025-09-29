# Dockerfile otimizado apenas para LangGraph
FROM python:3.11-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar arquivo de requirements otimizado
COPY requirements.txt .

# Atualizar pip e instalar dependências mínimas
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install "langgraph-cli[inmem]"

# Configurar variáveis de ambiente
ENV PYTHONPATH=/app
ENV PORT=8080

# Copiar apenas arquivos necessários
COPY src/ ./src/
COPY langgraph.json .

# Expor porta
EXPOSE 8080

# Comando para iniciar LangGraph
CMD ["langgraph", "dev", "--host", "0.0.0.0", "--port", "8080"]
