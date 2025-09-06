"""
Module: prompts/freeform_prompt.py

Build a system and user prompt for generating freeform (short-answer) exam questions.
"""


def build_freeform_prompt(context: str, category: str, difficulty: str, tags):
    """
    Create a system/user prompt pair for generating a short-answer exam question.

    Args:
        context (str): Few-shot examples in JSON format.
        category (str): Question category (e.g., "devops").
        difficulty (str): Difficulty level ("EASY", "MEDIUM", "HARD").
        tags (list): Domain tags, first element used as primary tag.

    Returns:
        tuple[str, str]: System prompt and user prompt strings.
    """
    prompt_system = """
Tu es un assistant pédagogique chargé de générer une **question d'examen à réponse libre directe** au format JSON.

Règles importantes :
- Ne sors JAMAIS du format JSON.
- JSON valide strictement conforme au schéma fourni, avec virgules entre les champs.
- La question doit porter sur une notion dont la réponse est unique, directe et vérifiable.
- Échapper correctement les guillemets et les antislashs.
"""

    prompt_user = f"""
Voici des exemples de questions précédentes :
{context}

Génère une **nouvelle question**, différente des exemples fournis, selon les critères suivants :
- Catégorie : {category}
- Difficulté : {difficulty}
- Tags : {tags[0]}

Le format JSON attendu est le suivant :

{{
  "question_type": "freeform",  
  "statement": "<p>Texte HTML de la question ici</p>",
  "category": "{category}",
  "difficulty": "{difficulty}",
  "score": 20 si EASY, 40 si MEDIUM, 60 si HARD,
  "time_limit": 40 si EASY, 60 si MEDIUM, 80 si HARD,
  "tags": "{tags[0]}",
  "help_description": "Un titre ou une courte description de l'objectif de la question",
  "validation_type": "Exact_Match",
  "exact_response": "Réponse correcte attendue ici"
}}
"""
    return prompt_system.strip(), prompt_user.strip()
