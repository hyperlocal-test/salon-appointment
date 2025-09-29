from langchain.schema import AIMessage
from langgraph.graph import MessagesState
from src.agents.helpers.common import FLOW_INTENT

def intent_location_node(data: MessagesState) -> MessagesState:
    """Processa a solicitação do usuário com base na intenção identificada."""

    last_message = data['messages'][-1] if data['messages'] else None
    
    content = f"""
        Que legal! Estamos localizados na Rua das Flores, 123, no centro da cidade. Nosso horário de funcionamento é de segunda a sexta-feira, das 9h às 18h, e aos sábados, das 9h às 14h. Se precisar de mais alguma informação, é só me avisar! 😊        
    """
    additional_kwargs = {
        **last_message.additional_kwargs,
        **{'step': FLOW_INTENT, 'end': True}
    }
    data['messages'].append(AIMessage(content=content, additional_kwargs=additional_kwargs))

    return data