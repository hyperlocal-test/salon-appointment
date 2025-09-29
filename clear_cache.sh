#!/bin/bash

# Script para limpar os caches e reiniciar o ambiente de desenvolvimento
# Execute: chmod +x clear_cache.sh && ./clear_cache.sh [PROD]
# Parâmetro PROD: Pula operações Docker para ambiente de produção

ENVIRONMENT=${1:-"DEV"}


echo "🧹 Limpando caches Python..."

# Limpar caches do pip, __pycache__ e arquivos .pyc
pip cache purge 2>/dev/null || echo "pip cache não disponível"

# Remover diretórios __pycache__ e arquivos .pyc
find . -type d -name "__pycache__" -delete 2>/dev/null || echo "Nenhum cache __pycache__ encontrado"

# Remover arquivos .pyc
find . -name "*.pyc" -delete 2>/dev/null || echo "Nenhum arquivo .pyc encontrado"

echo "✅ Caches Python limpos."

if [ "$ENVIRONMENT" != "PRD" ]; then
    echo "🐳 Parando e removendo containers..."
    docker compose down -v

    echo "🗑️ Removendo imagens e volumes..."
    docker system prune -a -f

    echo "🌐 Criando/verificando rede Docker..."
    docker network create network-hyperlocal 2>/dev/null || echo "Rede já existe"

    echo "🚀 Iniciando serviços..."
    if [ "$1" = "--api" ]; then
        echo "📡 Iniciando com FastAPI..."
        docker compose -f docker-compose-fastapi.yml up --build
    else
        echo "🐳 Iniciando configuração padrão..."
        docker compose up --build
    fi
else
    echo "🏭 Ambiente PROD detectado - Pulando operações Docker"
    echo "✅ Limpeza de cache concluída para produção"
fi