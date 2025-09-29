from langchain.schema import AIMessage, HumanMessage
from langgraph.graph import MessagesState

from src.agents.helpers.common import FLOW_INTENT, FLOW_CLASSIFIER

def intent_classifier_node(data: MessagesState) -> MessagesState:
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
        Percebi que você ainda não informou o que deseja fazer. Por favor, escolha uma opção, como: agendar, cancelar, consultar disponibilidade, verificar preços ou saber a localização.
    """
    additional_kwargs = {
        **last_message.additional_kwargs,
        **{'step': FLOW_INTENT, 'end': True}
    }
    data['messages'].append(AIMessage(content=content, additional_kwargs=additional_kwargs))

    return data
