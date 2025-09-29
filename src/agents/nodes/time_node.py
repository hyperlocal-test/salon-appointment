from langchain.schema import AIMessage, HumanMessage
from langgraph.graph import MessagesState

from src.agents.helpers.common import FLOW_TIME, FLOW_CLASSIFIER

def time_classifier_node(data: MessagesState) -> MessagesState:
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
        você informou a data, más não infomou a *hora*, peço que informe a HORA para quando deseja seu serviço.
    """
    additional_kwargs = {
        **last_message.additional_kwargs,
        **{'step': FLOW_TIME, 'end': True}
    }
    data['messages'].append(AIMessage(content=content, additional_kwargs=additional_kwargs))

    return data