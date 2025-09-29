from langchain.schema import AIMessage
from langgraph.graph import MessagesState

def cond_identifier(data: MessagesState) -> MessagesState:
    last_message = data['messages'][-1] if data['messages'] else None
    additional_kwargs = last_message.additional_kwargs if last_message else {}

    if additional_kwargs.get('identifier'):
        identifier = additional_kwargs['identifier']
        flow = 'process_request'

        if identifier.get('intent') == 'N/A' :
            flow = 'intent'
        elif identifier.get('service') == 'N/A':
            flow = 'service'
        elif identifier.get('time') == 'N/A' and identifier.get('date') == 'N/A':
            flow = 'datetime'
        elif identifier.get('date') == 'N/A':
            flow = 'date'
        elif identifier.get('time') == 'N/A':
            flow = 'time'
            
    return flow