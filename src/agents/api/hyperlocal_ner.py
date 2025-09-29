import os
import requests
import json
from typing import Dict, Any, Optional


def call_hyperlocal_ner_api(text: str) -> Dict[str, Any]:
    """
    Chama a API NER do projeto hyperlocal para extrair entidades nomeadas do texto.
    
    Args:
        text (str): Texto a ser processado para extração de entidades
        
    Returns:
        Dict[str, Any]: Resposta da API contendo as entidades extraídas
        
    Raises:
        requests.RequestException: Erro na requisição HTTP
        ValueError: Erro de validação dos dados
    """
    
    # Capturar URL base do .env
    base_url = os.getenv("HYPERLOCAL_NER_API_URL", "http://hyperlocal-ner-app-1:80")
    
    # Se a URL do .env não tem porta, adicionar porta padrão
    if base_url and not ":" in base_url.split("//")[1]:
        base_url = f"{base_url}:80"
    
    api_endpoint = f"{base_url}/api/v1/ner"
    print(f"🌐 Chamando API NER: {api_endpoint}")
    print(f"📝 Texto para processar: '{text[:50]}{'...' if len(text) > 50 else ''}')")
    
    # Dados da requisição - verificar se API espera campos adicionais
    payload = {
        "text": text
    }
    
    # Validar entrada antes de enviar
    if not text or not isinstance(text, str):
        print(f"❌ Texto inválido: '{text}' (tipo: {type(text)})")
        return {
            "error": "invalid_input",
            "message": "Texto deve ser uma string não vazia",
            "entities": []
        }
    
    # Limpar texto - remover caracteres problemáticos
    text = text.strip()
    if len(text) == 0:
        print(f"❌ Texto vazio após limpeza")
        return {
            "error": "empty_text",
            "message": "Texto vazio após limpeza",
            "entities": []
        }
    
    # Verificar tamanho máximo (assumindo limite de 1000 caracteres)
    if len(text) > 1000:
        print(f"⚠️ Texto muito longo ({len(text)} chars), truncando...")
        text = text[:1000]
    
    # Headers da requisição
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:        
        print(f"📡 Enviando requisição para: {api_endpoint}")
        print(f"📦 Payload: {json.dumps(payload, ensure_ascii=False)}")
        
        # Fazer a requisição POST
        response = requests.post(
            url=api_endpoint,
            headers=headers,
            json=payload,
            timeout=30  # Timeout de 30 segundos
        )
        
        print(f"📨 Status da resposta: {response.status_code}")
        print(f"📄 Resposta: {response.text[:200]}...")
        
        # Verificar se a requisição foi bem-sucedida
        response.raise_for_status()
        
        # Parsear resposta JSON
        result = response.json()
        
        return result
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Erro de conexão com a API NER em {api_endpoint}")
        return {
            "error": "connection_error",
            "message": "Não foi possível conectar com a API NER",
            "entities": []
        }
        
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout na chamada da API NER")
        return {
            "error": "timeout_error", 
            "message": "API NER não respondeu no tempo esperado",
            "entities": []
        }
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP na API NER: {e}")
        print(f"📄 Status Code: {response.status_code}")
        print(f"📄 Resposta completa: {response.text}")
        print(f"📋 Headers enviados: {headers}")
        print(f"📋 Payload enviado: {json.dumps(payload, ensure_ascii=False)}")
        
        # Tentar parsear erro da API se for JSON
        try:
            error_detail = response.json()
            print(f"🔍 Detalhes do erro da API: {json.dumps(error_detail, indent=2, ensure_ascii=False)}")
        except:
            print("🔍 Resposta da API não é JSON válido")
        
        return {
            "error": "http_error",
            "message": f"API NER retornou erro HTTP: {response.status_code}",
            "status_code": response.status_code,
            "response_text": response.text,
            "entities": []
        }
        
    except json.JSONDecodeError:
        print(f"❌ Erro ao decodificar JSON da API NER")
        print(f"📄 Resposta raw: {response.text}")
        return {
            "error": "json_decode_error",
            "message": "Resposta da API NER não é um JSON válido",
            "entities": []
        }
        
    except Exception as e:
        print(f"❌ Erro inesperado na API NER: {e}")
        return {
            "error": "unexpected_error",
            "message": f"Erro inesperado: {str(e)}",
            "entities": []
        }


def extract_entities_async(text: str) -> Optional[Dict[str, Any]]:
    """
    Versão assíncrona da chamada da API NER (wrapper).
    
    Args:
        text (str): Texto para extração de entidades
        
    Returns:
        Optional[Dict[str, Any]]: Resultado da extração ou None em caso de erro
    """
    try:
        result = call_hyperlocal_ner_api(text)
        
        # Verificar se houve erro
        if "error" in result:
            print(f"⚠️ API NER retornou erro: {result['message']}")
            return None
            
        return result
        
    except Exception as e:
        print(f"❌ Erro na extração assíncrona: {e}")
        return None