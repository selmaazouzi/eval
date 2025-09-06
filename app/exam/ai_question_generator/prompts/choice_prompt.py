"""
Module: choice_prompt.py

Build a system and user prompt for generating multiple-choice exam questions (QCU/QCM).
"""


def build_choice_prompt(context: str, category: str, difficulty: str, tags, qtype: str):
    """
    Create a system/user prompt pair for generating a multiple-choice question.

    Args:
        context (str): Few-shot examples in JSON format.
        category (str): Question category (e.g., "devops").
        difficulty (str): Difficulty level ("EASY", "MEDIUM", "HARD").
        tags (list): Domain tags, first element used as primary tag.
        qtype (str): "QCU" (single answer) or "QCM" (multiple answers).

    Returns:
        tuple[str, str]: System prompt and user prompt strings.
    """
    prompt_system = """
Tu es un assistant pédagogique chargé de générer une **question d'examen à choix (QCM ou QCU)** au format JSON.

Règles importantes :
- Ne réutilise pas les anciennes questions.
- Ne sors JAMAIS du format JSON.
- JSON valide strictement conforme au schéma fourni, avec virgules entre les champs.
- Garde un style clair, académique, et strictement lié au domaine spécifié.
- Échapper correctement les guillemets et les antislashs.
"""
    prompt_user= f"""
Voici des exemples de questions précédentes :
{context}

Génère une **nouvelle question**, différente des exemples fournis, selon les critères suivants :
- Catégorie : {category}
- Difficulté : {difficulty}
- Tags : {tags[0]}
- Type : {qtype}

Le format JSON attendu est le suivant :

{{
  "question_type": "choice",
  "statement": "<p>Texte HTML de la question ici</p>",
  "category": "{category}",
  "difficulty": "{difficulty}",
  "score": 10 si EASY, 20 si MEDIUM, 30 si HARD,
  "time_limit": 40 si EASY, 60 si MEDIUM, 80 si HARD,
  "tags": "{tags[0]}",
  "help_description": "Un titre ou une courte description de l'objectif de la question",
  "type": "{qtype}",
  "answers": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"],
  "right_answer": "Réponse B"
}}
"""
    return prompt_system.strip(), prompt_user.strip()
