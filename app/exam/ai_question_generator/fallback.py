"""
Module: ai_question_generator/fallback.py

Attempts OpenRouter first, then falls back to local Ollama if it fails.

Usage:
    result = generate_with_fallback(system_msg, user_msg)
"""

import logging
from .ollama import call_ollama
from .openrouter import call_openrouter
logger = logging.getLogger(__name__)

def generate_with_fallback(system_msg: str, user_msg: str) -> dict:
    """
    Attempts to generate a JSON response using OpenRouter first.
    Falls back to a local Ollama instance if OpenRouter fails.

    Args:
        system_msg (str): The system-level instruction for the LLM.
        user_msg (str): The user query or task description.

    Returns:
        dict: Parsed JSON object returned by the chosen LLM.

    Raises:
        RuntimeError: If both OpenRouter and Ollama fail.
    """
    try:
        return call_openrouter(system_msg, user_msg)
    except Exception as e1:
        logger.warning(f"OpenRouter KO → fallback Ollama. Raison: {e1}")
        # Fallback
        try:
            return call_ollama(system_msg, user_msg)
        except Exception as e2:
            logger.error(f"Ollama KO après fallback. Raison: {e2}", exc_info=True)
            # Remonte l'erreur combinée pour observabilité
            raise RuntimeError(f"Echec primaire (OpenRouter): {e1} | Echec fallback (Ollama): {e2}")
