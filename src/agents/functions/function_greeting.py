function_greeting = [
    {
        "name": "greeting_validate",
        "description": "Valida se a entrada contém uma saudação",
        "parameters": {
            "type": "object",
            "properties": {
                "greeting": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista de saudações extraídas da entrada do usuário. Se a entrada não contiver uma saudação, a lista será vazia.",
                }
            },
            "required": ["greeting"],
        },
    }
]