import os
import json

from src.agents.helpers.connect_llm import llm_openai
from src.agents.helpers.comprehend import ComprehendIntentClassifier
from src.agents.helpers.hyperlocal_ner import HyperlocalNERClassifier
from src.agents.helpers.common import FLOW_INTENT, get_last_message_by_type, filter_field_entities

from langchain.schema import AIMessage, HumanMessage
from langgraph.graph import MessagesState


def classifier_node(data: MessagesState) -> MessagesState:
    """Classifica a intenção do usuário baseado na mensagem."""

    last_message = data['messages'][-1] if data['messages'] else None
    last_human_message = get_last_message_by_type(data['messages'], 'HumanMessage')

    # Validar se o conteúdo existe e tem o tipo correto
    if last_human_message.content:
        user_text = last_human_message.content.strip()
        
        intent_classifier = HyperlocalNERClassifier()
        result = intent_classifier.extract_entities(user_text)
        print("NER Result:", result)
        print("User Text:", user_text)

        if result:
            service = result['entities'].get('SERVICO', {}).get('text', 'N/A')
            intent = result.get('intention', 'N/A')
            time = filter_field_entities(result['entities'], 'HORARIO')
            date = filter_field_entities(result['entities'], 'DATA')
            additional_kwargs = last_message.additional_kwargs

            # Recuperar valores anteriores ou inicializar vazio
            existing_identifier = additional_kwargs.get('identifier', {})
            
            # Política de atualização incremental: preserva o que já foi identificado, atualiza apenas o que é novo
            final_service = service if service != 'N/A' else existing_identifier.get('service', 'N/A')
            final_intent = intent if intent != 'N/A' else existing_identifier.get('intent', 'N/A')
            final_time = time if time != 'N/A' else existing_identifier.get('time', 'N/A')
            final_date = date if date != 'N/A' else existing_identifier.get('date', 'N/A')

            additional_kwargs['identifier'] = {
                "service": final_service,
                "intent": final_intent,
                "time": final_time,
                "date": final_date
            }
            
            additional_kwargs['step'] = 'end'

            print("Identifier:", additional_kwargs['identifier'])

            data['messages'].append(AIMessage(content="", additional_kwargs={**additional_kwargs}))

            return data
    else:
        print(f"❌ Conteúdo inválido ou tipo não é texto: {last_human_message}")
        user_text = None

    data['messages'].append(AIMessage(content="Mensagem processada", additional_kwargs={'step': FLOW_INTENT, 'end': True}))

    return data
