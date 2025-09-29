from langchain.schema import AIMessage
from langgraph.graph import MessagesState
from src.agents.helpers.common import FLOW_PROCESS_REQUEST

def process_request_node(data: MessagesState) -> MessagesState:
    """Processa a solicitação do usuário com base na intenção identificada."""
    last_message = data['messages'][-1] if data['messages'] else None
    additional_kwargs = last_message.additional_kwargs if last_message else {}
    identifier = additional_kwargs.get('identifier', {})
    intent = identifier.get('intent', 'N/A')
    service = identifier.get('service', 'N/A')
    date = identifier.get('date', 'N/A')
    time = identifier.get('time', 'N/A')

    
    content = f"""
        Consegui coletar todas as informações necessárias para processar sua solicitação. Você solicitou:
        
        - Você Deseja: {intent}
        - Serviço: {service}
        - Data e Horário: {date} às {time}

        Você confirma essas informações?
    """
    additional_kwargs = {
        **last_message.additional_kwargs,
        **{'step': FLOW_PROCESS_REQUEST, 'end': True}
    }
    data['messages'].append(AIMessage(content=content, additional_kwargs=additional_kwargs))

    return data