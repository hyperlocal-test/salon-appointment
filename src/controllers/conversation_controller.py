from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from src.services.conversation_service import ConversationWithBot, ResponseConversation

chatRouter = APIRouter()

class ConversationRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

@chatRouter.post("/conversation", response_model=ResponseConversation, operation_id="conversation")
async def chat_endpoint(request: ConversationRequest) -> ResponseConversation:
    return ConversationWithBot(request.dict())