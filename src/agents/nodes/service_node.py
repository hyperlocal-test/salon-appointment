from langchain.schema import AIMessage, HumanMessage
from langgraph.graph import MessagesState

from src.agents.helpers.common import FLOW_SERVICE, FLOW_CLASSIFIER

def service_classifier_node(data: MessagesState) -> MessagesState:
    """Classifica a intenção do usuário baseado na mensagem."""
    last_message = data['messages'][-1] if data['messages'] else None

    if isinstance(last_message, HumanMessage):
        additional_kwargs = {
            **last_message.additional_kwargs,
            **{'step': FLOW_CLASSIFIER, 'end': False}
        }

        data['messages'].append(AIMessage(content="", additional_kwargs=additional_kwargs))

        return data
    
    content = """
        Certo, antes de continuarmos, preciso que informe um serviço. Escolha uma dessas opções: Corte de Cabelo, Sobrancelha, Depilação ou Depilação Completa.
    """
    additional_kwargs = {
        **last_message.additional_kwargs,
        **{'step': FLOW_SERVICE, 'end': True}
    }
    data['messages'].append(AIMessage(content=content, additional_kwargs=additional_kwargs))

    return data