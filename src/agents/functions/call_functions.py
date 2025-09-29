from src.agents.helpers.common import TypeGreeting

def greeting_validate(greeting: list[str]) -> dict:
    """
    Validate if the input string contains a greeting.
    """
    return {
        "formal_greeting": [c for c in greeting if c.lower() in  TypeGreeting()["formal_greeting"]],
        "informal_greeting": [c for c in greeting if c.lower() in  TypeGreeting()["informal_greeting"]],
    }