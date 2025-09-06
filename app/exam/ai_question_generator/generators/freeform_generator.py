"""
Module: generators/freeform_generator.py

Generate freeform short-answer exam questions using the RAG pipeline.
"""

from ..prompts import build_freeform_prompt
from ..fallback import generate_with_fallback

def generate_freeform_question(category: str, difficulty: str, tags, context: str):
    """
    Generate a freeform question in strict JSON format.

    Args:
        category (str): Question category (e.g., "devops", "networking").
        difficulty (str): Difficulty level ("EASY", "MEDIUM", "HARD").
        tags (list[str]): Keywords/topics (e.g., ["git"]).
        context (str): Retrieved contextual examples.

    Returns:
        dict or None: JSON-formatted question, or None if generation fails.
    """
    print(context)
    prompt_system, prompt_user = build_freeform_prompt(context, category, difficulty, tags)
    result = generate_with_fallback(prompt_system, prompt_user)
    return result