import re

# Word-count thresholds
_SHORT_PROMPT = 15
_LONG_PROMPT = 75

# Signals that suggest low complexity
_LOW_SIGNALS = [
    "what is", "what are", "who is", "where is", "when is", "when was",
    "define", "definition of", "yes or no", "true or false", "how many", "how much",
    "list the", "name the",
]

# Signals that suggest medium complexity
_MEDIUM_SIGNALS = [
    "explain", "describe", "summarize", "summarise", "compare", "contrast",
    "what is the difference", "why does", "why is", "how does", "how do",
    "pros and cons", "advantages", "disadvantages", "step by step",
]

# Signals that suggest high complexity
_HIGH_SIGNALS = [
    "write a", "write an", "create a", "create an", "build a", "build an",
    "implement", "design a", "design an", "develop a", "develop an",
    "generate a", "generate an", "make a", "make an",
    "refactor", "debug", "fix the", "optimize", "write me", "draft a", "draft an", "compose a", "compose an", 
    "help me write", "help me create", "help me build", 
    "can you write", "could you write", "please write"
]


def classify_complexity(prompt: str) -> str:
    """
    Classify a prompt as 'low', 'medium', or 'high' complexity using heuristics.

    This is a fast, dependency-free classifier intended to guide model tier
    selection. It is not a perfect classifier — it errs on the side of routing
    borderline cases to a higher tier rather than a lower one.
    """
    lowered = prompt.lower()
    word_count = len(prompt.split())

    # --- Hard high-complexity signals ---
    # Code blocks suggest structured output the user cares about
    has_code_block = "```" in prompt or "`" in prompt
    # Multiple questions suggest a compound / research task
    question_count = lowered.count("?")
    # Structured output requests
    has_structured_output = bool(re.search(
        r"\b(json|xml|csv|table|schema|class diagram|uml)\b", lowered
    ))
    # Numbered or bulleted lists in the prompt itself indicate multi-step instructions
    has_numbered_steps = bool(re.search(r"(\n\s*\d+[\.\)]|\n\s*[-*])", prompt))

    if (
        has_code_block
        or has_structured_output
        or has_numbered_steps
        or question_count >= 3
        or word_count > _LONG_PROMPT
        or any(sig in lowered for sig in _HIGH_SIGNALS)
    ):
        return "high"

    # --- Medium signals ---
    if (
        question_count == 2
        or _SHORT_PROMPT < word_count <= _LONG_PROMPT
        or any(sig in lowered for sig in _MEDIUM_SIGNALS)
    ):
        return "medium"

    # --- Low signals / short prompts ---
    if word_count <= _SHORT_PROMPT or any(sig in lowered for sig in _LOW_SIGNALS):
        return "low"

    # Default to medium rather than under-routing
    return "medium"
