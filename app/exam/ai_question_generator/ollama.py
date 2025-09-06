"""
Module: ai_question_generator/ollama.py

Handles interaction with a locally hosted Ollama instance for structured JSON generation.

Main Responsibilities:
- Send system and user prompts to an Ollama LLM.
- Request output in strict JSON format.
- Parse and validate the model's response.
"""

import requests
import json
from .config_ai import MODEL_NAME, OLLAMA_BASE_URL

def call_ollama(system_msg: str, user_msg: str):
    """
    Send prompts to a local Ollama instance and return a parsed JSON object.

    Args:
        system_msg: Instructions for the model (system role).
        user_msg: User query or generation request.

    Returns:
        Parsed JSON object from the model's response.

    Raises:
        HTTPError: If the API request fails.
        ValueError: If the response is not valid JSON.
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        # Indice pour forcer JSON côté moteur (supporté par Ollama sur la plupart des modèles)
        "format": "json",
        "options": {"temperature": 0.2}
    }
    r = requests.post(url, json=payload)
    r.raise_for_status()
    data = r.json()
    # Selon Ollama, le contenu se trouve ici :
    txt = data["message"]["content"].strip()
    if not (txt.startswith("{") and txt.endswith("}")):
        raise ValueError("Ollama: la réponse n'est pas un objet JSON pur.")
    return json.loads(txt)
