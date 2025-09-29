# Flow names
FLOW_GREETING = "GREETING"
FLOW_CLASSIFIER = "CLASSIFIER"
FLOW_INTENT = "INTENT"
FLOW_SERVICE = "SERVICE"
FLOW_DATETIME = "DATETIME"
FLOW_DATE = "DATE"
FLOW_TIME = "TIME"
FLOW_PROCESS_REQUEST = "PROCESS_REQUEST"

# Intent
INTENT_CANCEL = "CANCELAR"
INTENT_SCHEDULE = "AGENDAR"
INTENT_PRICE = "PREÇOS"
INTENT_LOCATION = "LOCALIZAÇÃO"
INTENT_INQUIRY = "CONSULTA"

INTENTS = ['Agendamento', 'Cancelamento', 'Preços', 'Localização', 'Consulta']
SERVICES = ['Corte de Cabelo', 'Barba', 'Sobrancelha']

def TypeGreeting() -> dict:
    """
    Identify the type of greeting in the input string.
    """
    return {
        "formal_greeting": ["bom dia", "boa tarde", "boa noite"],
        "informal_greeting": ["olá", "oi", "e ai" , "salve", "saudações", "saudações!"]
    }

def get_last_message_by_type(messages: list, message_type: str):
    """
    Identifica a última mensagem conforme o tipo especificado.
    
    Args:
        messages (list): Array de mensagens do LangChain
        message_type (str): Tipo da mensagem ('AIMessage' ou 'HumanMessage')
    
    Returns:
        object: Última mensagem do tipo especificado ou None se não encontrar
    """
    if not messages:
        return None
    
    # Iterar de trás para frente para pegar a última mensagem do tipo
    for message in reversed(messages):
        if type(message).__name__ == message_type:
            return message
    
    return None

def filter_field_entities(entities, field: str) -> str:
    """
    Filtra entidades por um campo específico.
    
    Args:
        entities: Dicionário ou lista de entidades
        field (str): Campo para filtrar (ex: 'HORARIO', 'DATA')
    
    Returns:
        str: Valor formatado do campo ou 'N/A' se não encontrado
    """
    
    # Se for um dicionário (formato atual), buscar diretamente pela chave
    if isinstance(entities, dict):
        entity = entities.get(field)
        
        if not entity:
            return 'N/A'
        
        if field == 'HORARIO':
            # Procurar por converted_time primeiro, senão converted_date
            converted_time = entity.get('converted_time')
            if converted_time:
                return converted_time.get('formatted_time', 'N/A')
            return 'N/A'
        
        if field == 'DATA':
            converted_date = entity.get('converted_date')
            if converted_date:
                return converted_date.get('formatted_date', 'N/A')
            return 'N/A'
        
        # Para outros campos, retornar o texto da entidade
        return entity.get('text', 'N/A')
    
    # Se for uma lista (formato antigo), manter lógica anterior
    elif isinstance(entities, list):
        entity = next((e for e in entities if isinstance(e, dict) and e.get('label') == field), None)
        
        if not entity:
            return 'N/A'
        
        if field == 'HORARIO':
            return entity.get('converted_time', {}).get('formatted_time', 'N/A') if entity.get('converted_time') else 'N/A'
        
        if field == 'DATA':
            return entity.get('converted_date', {}).get('formatted_date', 'N/A') if entity.get('converted_date') else 'N/A'
        
        return entity.get('text', 'N/A')
    
    # Se não for nem dict nem list
    else:
        print(f"❌ Erro: entities deve ser uma lista ou dicionário, recebido: {type(entities)}")
        return 'N/A'


