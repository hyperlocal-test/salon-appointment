from src.agents.helpers.common import TypeGreeting
from src.agents.functions.function_greeting import function_greeting
from src.agents.helpers.connect_llm import llm_openai
from src.agents.functions.call_functions import greeting_validate
from src.agents.helpers.common import FLOW_INTENT, FLOW_CLASSIFIER

from langchain_core.messages import SystemMessage, HumanMessage
from langchain.schema import AIMessage
from langgraph.graph import MessagesState

import json


def response_greeting(type: str) -> str:
    """
    Gera uma resposta de saudação baseada no tipo (formal/informal)
    
    Args:
        type (str): Tipo da saudação - "formal" ou "informal"
    
    Returns:
        str: Mensagem de saudação personalizada
    """
    llm = llm_openai(model="gpt-4", temperature=0.2)

    # Determinar o tipo de saudação específico
    greeting_type = "formal" if type == "formal" else "informal"
    
    system_content = f"""
        Você é um assistente virtual chamado Stella, responsável por realizar agendamentos no nosso salão de beleza.

        TAREFA: Gere uma saudação do tipo {greeting_type.upper()}.

        TEMPLATE OBRIGATÓRIO:
        "<greeting>. Sou a Stella, assistente virtual do salão de beleza. Como posso ajudar você hoje?"

        SUBSTITUIÇÃO de <greeting>:
        - Se {greeting_type}: use {TypeGreeting()[f"{greeting_type}_greeting"]}
        
        INSTRUÇÕES:
        1. Use APENAS uma saudação do tipo solicitado
        2. Mantenha o template exato
        3. Seja natural e acolhedora
        4. Resposta em uma única frase completa
        
        EXEMPLO DE RESPOSTA:
        "{TypeGreeting()[f"{greeting_type}_greeting"]}. Sou a Stella, assistente virtual do salão de beleza. Como posso ajudar você hoje?"
    """

    messages = [SystemMessage(content=system_content)]
    
    try:
        response = llm.invoke(messages)
        return response.content.strip()
    except Exception as e:
        # Fallback em caso de erro
        greeting = TypeGreeting()[f"{greeting_type}_greeting"]
        return f"{greeting}. Sou a Stella, assistente virtual do salão de beleza. Como posso ajudar você hoje?"

def greeting_identify(data: MessagesState) -> MessagesState:
    """
    Identify the greeting in the message and respond accordingly.
    """
    if len(data['messages']) == 1 and isinstance(data['messages'][0], HumanMessage):
        last_message = data['messages'][-1] if data['messages'] else None

        system_prompt =  f"""
            Você é um agente de saudação. Sua tarefa é identificar a saudação na mensagem do usuário.
            A saudação pode ser identificada no começo, meio ou no fim da frase.

            Exemplos:
            - {TypeGreeting()["formal_greeting"]}
            - {TypeGreeting()["informal_greeting"]}
        """

        # Usar ChatOpenAI do LangChain
        llm = llm_openai(model="gpt-4", temperature=0)
        
        # Converter para mensagens do LangChain
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=last_message.content)
        ]
        
        # Usar função binding para function calling no LangChain
        llm_with_functions = llm.bind(
            functions=function_greeting,
            function_call={"name": "greeting_validate"}
        )
        
        response = llm_with_functions.invoke(messages)
        
        # Extrair argumentos da função
        if hasattr(response, 'additional_kwargs') and 'function_call' in response.additional_kwargs:
            arguments = response.additional_kwargs['function_call']['arguments']
            args = json.loads(arguments)
        else:
            # Fallback se não houver function call
            args = {"greeting": "formal"}
        result = greeting_validate(args['greeting'])

        message_greeting = "Olá! Como posso ajudá-lo hoje?"

        if result['formal_greeting']:
            message_greeting = response_greeting("formal")
        elif result['informal_greeting']:
            message_greeting = response_greeting("informal")

        # Garantir que message_greeting não seja None ou vazio
        if not message_greeting or message_greeting.strip() == "":
            message_greeting = "Olá! Como posso ajudá-lo hoje?"

        ai_message = AIMessage(
            content=message_greeting.strip(),
            additional_kwargs={'step': FLOW_CLASSIFIER, 'end': False}
        )
        data['messages'].append(ai_message)

    return data