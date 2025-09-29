from langgraph.graph import END

def add_conditional_flow_edges(workflow, sources, cond_flow):
    for source in sources:
        workflow.add_conditional_edges(
            source,
            cond_flow,
            {
                "greeting": "GreetingIdentify",
                "classifier": "Classifier",
                "intent": "IntentClassifier",
                "service": "ServiceClassifier",
                "datetime": "DateTimeClassifier",
                "date": "DateClassifier",
                "time": "TimeClassifier",
                "process_request": "ProcessRequest",
                "end": END,
            }
        )