from flask import Blueprint, request, Response
from src.va.services.chat_service import ChatService

ai_chat = Blueprint('openai', "chatty")

chat_service = ChatService()

@ai_chat.route("/chat", methods=['POST'])
def chat() -> Response:
    return chat_service.chat(request=request)

@ai_chat.route("/conversation", methods=['POST'])
def conversation() -> Response:
    return chat_service.conversation(request=request)
