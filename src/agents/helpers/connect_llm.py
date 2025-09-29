import os
from langchain_openai import ChatOpenAI

def llm_openai(model: str = os.getenv("OPENAI_MODEL", "gpt-4"), temperature: float = None, max_tokens: int = None, streaming: bool = False) -> ChatOpenAI:
    """
    Conecta diretamente com a OpenAI API
    
    Args:
        model (str): Nome do modelo OpenAI (ex: gpt-4, gpt-3.5-turbo, gpt-4-turbo)
        temperature (float): Controla a criatividade das respostas (0.0 a 2.0). None usa padrão do modelo.
        max_tokens (int): Número máximo de tokens na resposta
        streaming (bool): Habilita ou desabilita o streaming de respostas
    Returns:
        ChatOpenAI: Instância configurada do ChatOpenAI
    """
    
    # Modelos que só suportam temperatura padrão (1.0)
    models_fixed_temp = ["gpt-5-mini", "gpt-o1", "gpt-o1-preview", "gpt-o1-mini"]
    
    # Configuração base
    config = {
        "model": model,
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "streaming": streaming
    }
    
    # Adicionar max_tokens apenas se especificado
    if max_tokens is not None:
        config["max_tokens"] = max_tokens
    
    # Tratar temperatura baseado no modelo
    if model in models_fixed_temp:
        # Não adicionar temperatura para estes modelos
        pass
    else:
        # Para outros modelos, usar temperatura especificada ou padrão 0.7
        temp_value = temperature if temperature is not None else 0.7
        config["temperature"] = temp_value
    
    return ChatOpenAI(**config)