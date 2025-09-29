from langchain.schema import HumanMessage, AIMessage
from langchain_community.chat_message_histories import FileChatMessageHistory
from src.agents.helpers.common import FLOW_GREETING
from typing import TypedDict, Literal, NotRequired
from typing import List
import os

# Variável global para o diretório de armazenamento do histórico
HISTORY_STORAGE_PATH = "./src/history/storage/"

# Garante que o diretório existe
os.makedirs(HISTORY_STORAGE_PATH, exist_ok=True)

class ResponseConversation(TypedDict):
    user_id: NotRequired[str]
    messages: NotRequired[List[dict]]

class HistoryService:

    @staticmethod
    def set_user_message(chat_history: FileChatMessageHistory, content: str, additional_kwargs: dict) -> None:
        """
        Adiciona uma mensagem do usuário ao histórico de chat.
        """
        user_msg = HumanMessage(
            content=content,
            additional_kwargs={**additional_kwargs}
        )

        chat_history.add_user_message(user_msg)

    @staticmethod
    def set_ai_message(chat_history: FileChatMessageHistory, content: str, additional_kwargs: dict) -> None:
        """
        Adiciona uma mensagem da IA ao histórico de chat.
        """
        ai_msg = AIMessage(
            content=content,
            additional_kwargs={**additional_kwargs}
        )

        chat_history.add_ai_message(ai_msg)

    @staticmethod
    def clear_history(session_id: str) -> None:
        file_path = os.path.join(HISTORY_STORAGE_PATH, f"history-{session_id}.json")
        chat_history = FileChatMessageHistory(file_path=file_path)
        chat_history.clear()

    @staticmethod
    def get_history(session_id: str, content: str) -> FileChatMessageHistory:
        # 1. Carrega ou cria histórico usando path global
        file_path = os.path.join(HISTORY_STORAGE_PATH, f"history-{session_id}.json")
        chat_history = FileChatMessageHistory(file_path=file_path)

        # 2. Adiciona nova mensagem do usuário
        if len(chat_history.messages) == 0:
            HistoryService.set_user_message(chat_history, content, additional_kwargs={'step': FLOW_GREETING})
        else:
            additional_kwargs = {**chat_history.messages[-1].additional_kwargs, **{'end': False}}
            HistoryService.set_user_message(chat_history, content, additional_kwargs=additional_kwargs)

        return chat_history