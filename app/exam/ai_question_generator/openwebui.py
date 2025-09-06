"""
Module: ai_question_generator/openwebui.py

Provides a helper to send prompts to an OpenWebUI LLM endpoint, with optional
vector-collection context.

Main Responsibilities:
- Build and send requests to the OpenWebUI API.
- Optionally attach a knowledge base ID for context retrieval.
- Return generated model output as text.
"""


import requests
from .config_ai import OWUI_TOKEN, MODEL_NAME, OPENWEBUI_URL  # Configuration values

def query_openwebui(prompt: str, knowledge_id=None):
    """
    Query an OpenWebUI LLM endpoint.

    Args:
        prompt: Prompt text to send to the model.
        knowledge_id: Optional vector-collection ID for contextual retrieval.

    Returns:
        Model's generated content, or None if the request fails.
    """
    headers = {
        "Authorization": f"Bearer {OWUI_TOKEN}",
        "Content-Type": "application/json"
    }

    # Construct payload for OpenWebUI's chat endpoint
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }

    # Attach external knowledge base if provided
    if knowledge_id:
        payload["files"] = [{"type": "collection", "id": knowledge_id}]

    try:
        # Make API call to OpenWebUI
        response = requests.post(OPENWEBUI_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Erreur OpenWebUI :", e)
        return None
