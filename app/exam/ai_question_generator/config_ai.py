"""
Module: ai_question_generator/config_ai.py

Centralized configuration for connecting to LLM APIs (OpenWebUI, OpenRouter, Ollama) 
used in the RAG pipeline.

Responsibilities:
- Load API keys and tokens from environment variables.
- Define API endpoints for local and remote LLM services.
- Specify the default models for each service.

This module ensures all credentials and runtime settings are in one place, 
making it easy to update without modifying core logic.
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ==========================
# Authentication Credentials
# ==========================
OWUI_TOKEN = os.getenv("OWUI_TOKEN")                # Token for OpenWebUI API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") # API key for OpenRouter

# ==========================
# OpenWebUI Configuration
# ==========================
MODEL_NAME = "mistral:latest"  # Local LLM model name (OpenWebUI or Ollama)
OPENWEBUI_URL = "http://localhost:3000/api/chat/completions"

# ==========================
# OpenRouter Configuration
# ==========================
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct:free"
# Alternative: "mistralai/mistral-7b-instruct:free" (free tier)

# ==========================
# Ollama Configuration
# ==========================
OLLAMA_BASE_URL = "http://localhost:11434"
