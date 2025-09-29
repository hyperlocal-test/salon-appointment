from typing import TypedDict, Optional, Dict, NotRequired

class ConversationState(TypedDict):
    message: str  # Campo obrigatório (vem do InitConversationState)
    user_id: Optional[str]  # Opcional inicialmente
    intent: Optional[str]
    entities: Optional[Dict[str, Optional[str]]]
    status: Optional[str]
    last_node: Optional[list[Optional[str]]]
    retries: Optional[int]
    response: Optional[str]  # Resposta gerada para o usuário
    flow: NotRequired[str]