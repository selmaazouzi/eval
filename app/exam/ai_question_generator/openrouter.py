"""
Module: ai_question_generator/openrouter.py

Handles interaction with the OpenRouter API for structured JSON generation.

Main Responsibilities:
- Send system and user prompts to an OpenRouter LLM.
- Enforce JSON object output format.
- Parse and validate the model's response.
"""

import requests
import json
from .config_ai import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_URL

def call_openrouter(prompt_system: str, prompt_user: str) -> dict:
    """
    Send system and user prompts to OpenRouter and return a parsed JSON object.

    Args:
        prompt_system: Instructions for the model (system role).
        prompt_user: User query or generation request.

    Returns:
        Parsed JSON object from the model's response.

    Raises:
        HTTPError: If the API request fails.
        ValueError: If the response is not valid JSON.
    """
    # Define headers including authorization and optional metadata
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",  # Optional referer for API usage context
        "X-Title": "exam-generator"          # Optional title shown in OpenRouter dashboard
    }

    # Construct the payload to send to the OpenRouter chat endpoint
    payload = {
        "model": OPENROUTER_MODEL,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user},
        ],
        "temperature": 0.6  # Controls randomness of the output
    }

    # Send the request to OpenRouter's API
    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload
    )

    # Raise an exception for any HTTP error (e.g., 4xx or 5xx)
    response.raise_for_status()

    # Return the generated content from the first choice
    txt = response.json()["choices"][0]["message"]["content"].strip()

    # Sécurité JSON: doit être un objet pur
    if not (txt.startswith("{") and txt.endswith("}")):
        raise ValueError("La réponse n'est pas un objet JSON pur.")

    try:
        data = json.loads(txt)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide: {e}") from e

    return data
