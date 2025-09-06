"""
Module: choice_generator.py

Generate multiple-choice exam questions (QCU/QCM) using the RAG pipeline.
"""

from ..prompts import build_choice_prompt
from ..fallback import generate_with_fallback
def generate_choice_question(category: str, difficulty: str, tags, qtype: str, context: str):
    """
    Generate a multiple-choice question in strict JSON format.

    Args:
        category (str): Question category (e.g., "frontend").
        difficulty (str): Difficulty level ("EASY", "MEDIUM", "HARD").
        tags (list[str]): Keywords/topics (e.g., ["reactjs"]).
        qtype (str): "QCU" (single answer) or "QCM" (multiple answers).
        context (str): Retrieved contextual examples.

    Returns:
        dict or None: JSON-formatted question, or None if generation fails.
    """
    prompt_system, prompt_user = build_choice_prompt(context, category, difficulty, tags, qtype)
    result = generate_with_fallback(prompt_system, prompt_user)
    return result