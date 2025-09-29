from langgraph.graph import StateGraph, MessagesState
from src.states.conversation_state import ConversationState

# Nodes
from src.agents.nodes.classifier_node import classifier_node

# Flows
from src.agents.nodes.start_flow import start_flow
from src.agents.nodes.greeting_node import greeting_identify
from src.agents.nodes.intent_node import intent_classifier_node
from src.agents.nodes.service_node import service_classifier_node
from src.agents.nodes.datetime_node import datetime_classifier_node
from src.agents.nodes.date_node import date_classifier_node
from src.agents.nodes.time_node import time_classifier_node
from src.agents.nodes.process_request_node import process_request_node

#Flow Intents
from src.agents.nodes.intent_cancel_node import intent_cancel_node
from src.agents.nodes.intent_price_node import intent_price_node
from src.agents.nodes.intent_location_node import intent_location_node

# Conditional flow helper
from src.agents.helpers.add_conditional_dynamics import add_conditional_flow_edges
from src.agents.condicional.cond_flow import cond_flow
from src.agents.condicional.cond_identifier import cond_identifier

# Criar o grafo - usando MessagesState para conversação
graph = StateGraph(MessagesState)

# Adicionar nós
graph.add_node("Classifier", classifier_node)
graph.add_node("IntentClassifier", intent_classifier_node)
graph.add_node("IntentCancel", intent_cancel_node)
graph.add_node("IntentPrice", intent_price_node)
graph.add_node("IntentLocation", intent_location_node)
graph.add_node("ServiceClassifier", service_classifier_node)
graph.add_node("DateTimeClassifier", datetime_classifier_node)
graph.add_node("DateClassifier", date_classifier_node)
graph.add_node("TimeClassifier", time_classifier_node)
graph.add_node("ProcessRequest", process_request_node)

graph.add_node("StartFlow", start_flow)
graph.add_node("GreetingIdentify", greeting_identify)

# Adicionar arestas
graph.add_edge("GreetingIdentify", "StartFlow")
graph.add_edge("IntentClassifier", "StartFlow")
graph.add_edge("ServiceClassifier", "StartFlow")
graph.add_edge("DateTimeClassifier", "StartFlow")
graph.add_edge("DateClassifier", "StartFlow")
graph.add_edge("TimeClassifier", "StartFlow")


# Definição do fluxo conversacional
add_conditional_flow_edges(
    graph,
    ["StartFlow"],
    cond_flow
)

graph.add_conditional_edges(
    "Classifier", 
    cond_identifier,
    {
        "intent": "IntentClassifier",
        "intent_cancel": "IntentCancel",
        "intent_price": "IntentPrice",
        "intent_location": "IntentLocation",
        "service": "ServiceClassifier",
        "datetime": "DateTimeClassifier",
        "date": "DateClassifier",
        "time": "TimeClassifier",
        "process_request": "ProcessRequest",
    }
)

# Ponto de entrada
graph.set_entry_point("StartFlow")

# Compilar o grafo
app_graph = graph.compile()