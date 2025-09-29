from langchain.schema import AIMessage
from langgraph.graph import MessagesState
from src.agents.helpers.common import FLOW_INTENT

def intent_price_node(data: MessagesState) -> MessagesState:
    """Processa a solicitação do usuário com base na intenção identificada."""

    last_message = data['messages'][-1] if data['messages'] else None
    
    content = f"""
        Vamos lá, segue nossa lista de valores de acordo com os serviços oferecidos:

        - Corte de Cabelo: R$ 50,00
        - Sobrancelha: R$ 30,00
        - Depilação: R$ 70,00
        - Depilação Completa: R$ 120,00

        obs: Esses podem ser extrair via API futuramente. Quem sabe depois que eu for efetivado, eu consiga te ajudar com isso, ok? 😁😁😁        
    """
    additional_kwargs = {
        **last_message.additional_kwargs,
        **{'step': FLOW_INTENT, 'end': True}
    }
    data['messages'].append(AIMessage(content=content, additional_kwargs=additional_kwargs))

    return data