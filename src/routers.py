from fastapi import APIRouter
from src.controllers.conversation_controller import chatRouter

api_router = APIRouter()

api_router.include_router(chatRouter, tags=["Conversation"])