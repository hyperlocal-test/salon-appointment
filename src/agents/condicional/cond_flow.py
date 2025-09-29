from src.states.conversation_state import ConversationState

def cond_flow(data: ConversationState) -> str:    
    return data['flow']