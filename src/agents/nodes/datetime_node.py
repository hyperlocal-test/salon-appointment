from langchain.schema import AIMessage, HumanMessage
from langgraph.graph import MessagesState

from src.agents.helpers.common import FLOW_DATETIME, FLOW_CLASSIFIER

def datetime_classifier_node(data: MessagesState) -> MessagesState:
    """Classifica a intenção do usuário baseado na mensagem."""
    last_message = data['messages'][-1] if data['messages'] else None

    print("Datetime Node - Last Message Type:", type(last_message))
    print(last_message)

    if isinstance(last_message, HumanMessage):
        print("✅ Datetime Recebida.")

        additional_kwargs = {
            **last_message.additional_kwargs,
            **{'step': FLOW_CLASSIFIER, 'end': False}
        }

        data['messages'].append(AIMessage(content="", additional_kwargs=additional_kwargs))

        return data
    
    content = """
        Legal, já consegui identificar o serviço e o que você deseja. Agora preciso que me informe a data e o horário para prosseguirmos.
    """
    additional_kwargs = {
        **last_message.additional_kwargs,
        **{'step': FLOW_DATETIME, 'end': True}
    }
    data['messages'].append(AIMessage(content=content, additional_kwargs=additional_kwargs))

    return data