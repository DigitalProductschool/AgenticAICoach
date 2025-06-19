def format_chat_history(chat_history: list[dict[str, str]]) -> str:
    if not chat_history:
        return "This is the start of our conversation."
    formatted = "\n".join(
        f"User: {entry['user']}\nCoach: {entry['assistant']}"
        for entry in chat_history
    )
    return formatted.replace('â€"', '-').replace('â€™', "'").replace('â€œ', '"').replace('â€', '"')
