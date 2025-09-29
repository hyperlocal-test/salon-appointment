from src.states.conversation_state import ConversationState
from langgraph.graph import MessagesState
from src.agents.helpers.common import FLOW_GREETING, FLOW_CLASSIFIER, FLOW_SERVICE, FLOW_PROCESS_REQUEST, FLOW_INTENT, FLOW_DATETIME, FLOW_DATE, FLOW_TIME

def start_flow(data: MessagesState) -> MessagesState:
    """
    Inicia o fluxo com base na última mensagem do usuário.

    Args:
        data (ConversationState): Informações fornecidas pelo usuário e processadas internamente.

    Returns:
        dict: Resposta estruturada do agente.
    """
    last_message = data['messages'][-1] if data['messages'] else None
    
     # Verifica se o fluxo será encerrado
    if "end" in last_message.additional_kwargs and last_message.additional_kwargs['end']:
        data['flow'] = 'end'
        return data
    
    if not last_message or 'step' not in last_message.additional_kwargs or last_message.additional_kwargs['step'] == FLOW_GREETING:
        data['flow'] = 'greeting'
    elif last_message.additional_kwargs['step'] == FLOW_CLASSIFIER:
        data['flow'] = 'classifier'
    elif last_message.additional_kwargs['step'] == FLOW_INTENT:
        data['flow'] = 'intent'
    elif last_message.additional_kwargs['step'] == FLOW_SERVICE:
        data['flow'] = 'service'
    elif last_message.additional_kwargs['step'] == FLOW_DATETIME:
        data['flow'] = 'datetime'
    elif last_message.additional_kwargs['step'] == FLOW_DATE:
        data['flow'] = 'date'
    elif last_message.additional_kwargs['step'] == FLOW_TIME:
        data['flow'] = 'time'
    elif last_message.additional_kwargs['step'] == FLOW_PROCESS_REQUEST:
        data['flow'] = 'process_request'
    else:
        data['flow'] = 'end'

    return data