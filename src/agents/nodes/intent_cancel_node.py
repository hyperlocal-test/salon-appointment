from langchain.schema import AIMessage
from langgraph.graph import MessagesState
from src.agents.helpers.common import FLOW_INTENT

def intent_cancel_node(data: MessagesState) -> MessagesState:
    """Processa a solicitação do usuário com base na intenção identificada."""

    last_message = data['messages'][-1] if data['messages'] else None
    
    content = f"""
        Identifiquei que você deseja cancelar um serviço, más neste momento não vou conseguir realizar o cancelamento. Por favor, entre em contato diretamente com o estabelecimento para efetuar o cancelamento.
        
        Quem sabe depois que eu for efetivado, eu consiga te ajudar com isso, ok? 😁😁😁
    """
    additional_kwargs = {
        **last_message.additional_kwargs,
        **{'step': FLOW_INTENT, 'end': True}
    }
    data['messages'].append(AIMessage(content=content, additional_kwargs=additional_kwargs))

    return data