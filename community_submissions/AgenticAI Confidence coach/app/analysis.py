import re

def analyze_text(text: str) -> dict:
    """
    Analyze text for low-confidence patterns.
    Returns a dictionary with counts of various confidence-related linguistic patterns.
    """
    # Define patterns for low-confidence indicators
    patterns = {
        "hedging": r"\b(just|maybe|perhaps|might|I think|I feel|not sure|mess up|wrong)\b",
        "apologizing": r"\b(sorry|apologize|I’m afraid|forgive me)\b",
        "minimizing": r"\b(only|merely|a little|somewhat|not much)\b",
        "passive_voice": r"\b(was|were|is|been|being)\b .* by\b",
        "excessive_qualification": r"\b(I’m not sure|I think|I guess|I believe|maybe|possibly)\b",
        "evasive_language": r"\b(I don’t know|I’m not an expert|I could be wrong|It’s possible that)\b",
        "understatements": r"\b(Okay|fine|not bad|could be worse)\b",
        "disclaimers": r"\b(Just my opinion|I’m no expert|This might be wrong|not capable)\b",
        "non_committal": r"\b(kind of|sort of|like|a bit|little)\b",
        "overuse_of_idk": r"\b(I don’t know| I have no idea| I am not confident)\b",
    }

    # Initialize results
    analysis_results = {
        "hedging_count": 0,
        "apologizing_count": 0,
        "minimizing_count": 0,
        "passive_voice_count": 0,
        "excessive_qualification_count": 0,
        "evasive_language_count": 0,
        "understatements_count": 0,
        "disclaimers_count": 0,
        "non_committal_count": 0,
        "overuse_of_idk_count": 0,
        "total_issues": 0,
    }

    for cue, pattern in patterns.items():
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        count = len(matches)
        analysis_results[f"{cue}_count"] = count
        analysis_results["total_issues"] += count

    return analysis_results