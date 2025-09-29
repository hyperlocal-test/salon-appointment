from src.history.history_service import HistoryService
from src.agents.index import app_graph
from langgraph.graph import MessagesState
from langchain.schema import AIMessage, HumanMessage
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel

class ConversationMessage(BaseModel):
    """Estrutura de uma mensagem individual na conversa."""
    type: Literal["text", "buttons"]
    content: str
    buttons: Optional[List[str]] = None

class ResponseConversation(BaseModel):
    """Estrutura de resposta da conversa compatível com FastAPI/Pydantic."""
    user_id: str
    messages: List[ConversationMessage]

def ConversationWithBot(user_query: Dict[str, Any]) -> ResponseConversation:
    session_id = user_query.get("session_id")
    message_content = user_query.get("message", "")

    if message_content == "#clear#":
        # Limpa o histórico de mensagens para a sessão
        HistoryService.clear_history(session_id=session_id)
        clear_message = ConversationMessage(
            type="text", 
            content="Histórico de conversa limpo."
        )
        return ResponseConversation(
            user_id=session_id,
            messages=[clear_message]
        )

    # Obtém o histórico (FileChatMessageHistory object) e adiciona a nova mensagem do usuário
    chat_history = HistoryService.get_history(
        session_id=session_id,
        content=message_content
    )

    # 1. Monta o estado MessagesState para o grafo usando as mensagens do histórico
    messages_state: MessagesState = {
        "messages": chat_history.messages  # Lista de HumanMessage/AIMessage do FileChatMessageHistory
    }

    # 2. Executa o fluxo LangGraph com MessagesState
    result = app_graph.invoke(messages_state)

    if result is None:
        raise ValueError("Desculpe, mas não foi possível processar sua solicitação neste momento.")
    
    messages = []
    messages_content = []

    for message in reversed(result['messages']):
        # if message.type != "ai":
        if not isinstance(message, AIMessage):
            break

        if not message.content:
            continue

        if message.additional_kwargs.get('buttons', None) is not None:
            messages_content.append({
                "type": "buttons",
                "content": message.content.strip(),
                "buttons": message.additional_kwargs['buttons']
            })
        else:
            messages_content.append({
                "type": "text",
                "content": message.content.strip()
            }) 
        
        messages.append(message)

    for message in reversed(messages):
        # 3. Adiciona a mensagem da IA ao histórico
        HistoryService.set_ai_message(
            chat_history=chat_history,
            content=message.content.strip(),
            additional_kwargs=message.additional_kwargs or {}
        )

    # Inverter messages_content para ordem cronológica e converter para Pydantic
    messages_content = list(reversed(messages_content))
    conversation_messages = [
        ConversationMessage(**msg_dict) for msg_dict in messages_content
    ]
    
    return ResponseConversation(
        user_id=session_id,
        messages=conversation_messages
    )