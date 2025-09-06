"""
Module: code_generator.py

Generate programming exam questions (Java/backend) using the RAG pipeline.
"""

from ..prompts import build_code_prompt
from ..fallback import generate_with_fallback
def generate_code_question(category: str, difficulty: str, tags, context: str):
    """
    Generate a coding question in strict JSON format.

    Args:
        category (str): Domain category (e.g., "backend", "algorithms").
        difficulty (str): Difficulty level ("EASY", "MEDIUM", "HARD").
        tags (list[str]): Programming context tags (e.g., ["java"]).
        context (str): Retrieved contextual examples.

    Returns:
        dict or None: JSON-formatted coding question, or None if generation fails.
    """
    prompt_system, prompt_user = build_code_prompt(context, category, difficulty, tags)
    result = generate_with_fallback(prompt_system, prompt_user)
    return result