def format_chat_history(chat_history: list[dict[str, str]]) -> str:
    """
    Converts the structured chat history into a plain-text format suitable
    for feeding into LLM prompts or CrewAI task descriptions.
    """

    # If there's no history, return a default introduction
    if not chat_history:
        return "This is the start of our conversation."

    # Format each chat turn as "User: ..." and "Coach: ..."
    formatted = "\n".join(
        f"User: {entry['user']}\nCoach: {entry['assistant']}"
        for entry in chat_history
    )

    # Clean up common encoding issues
    return formatted.replace('â€"', '-').replace('â€™', "'").replace('â€œ', '"').replace('â€', '"')
