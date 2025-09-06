"""
Module: code_prompt.py

Builds system/user prompts for generating JSON-formatted programming exercises 
(Java-focused, extensible to other backend languages).
"""

import json

def build_code_prompt(context: str, category: str, difficulty: str, tags):
    """
    Create a system/user prompt pair for generating a coding question.

    Args:
        context (str): Few-shot examples in JSON format.
        category (str): Question category (e.g., "algorithms").
        difficulty (str): Difficulty level ("EASY", "MEDIUM", "HARD").
        tags (list): Domain tags (e.g., ["java", "oop"]).

    Returns:
        tuple[str, str]: System prompt and user prompt strings.
    """
  
    prompt_system = """
Tu es un assistant pédagogique chargé de générer des **questions d'examen de programmation (Java)** au format JSON strict.

Règles importantes :
- Ne sors JAMAIS du format JSON.
- Le JSON doit être valide (RFC 8259) et strictement conforme au schéma fourni.
- Utilise uniquement du HTML dans les champs textuels (`statement`, `initial_candidate_code`,
  `initial_candidate_test_code`, `validator_code`, `main_code`, `possible_solution`).
- Le code doit être clair, rigoureux et académique (indentation correcte, noms explicites).
- Échapper correctement les guillemets et les antislashs.
- Fournir le champ `validator_methods` comme un tableau de 4 sous-tableaux, chacun contenant :
  1) le nom exact de la méthode dans `validator_code` (ex: "validator1"),
  2) une courte description (titre),
  3) un entier représentant les points attribués à cette validation.
- La somme des points de `validator_methods` doit être égale à `score`.
"""
    prompt_user= f"""
Voici des exemples de questions précédentes :
{context}
Génère une nouvelle question, différente des exemples, selon les critères :
- Catégorie : {category}
- Difficulté : {difficulty}
- Tags : {tags}

Réponds UNIQUEMENT avec un objet JSON. Exemple de structure attendue (valeurs illustratives) :

{{
  "question_type": "code",
  "statement": "<p>Texte HTML du sujet de l'exercice ici</p>",
  "initial_candidate_code": "<p>Squelette de la classe et méthode à compléter.</p>",
  "initial_candidate_test_code": "<p>Classe Main contenant du code de test, les sorties affichées uniquement entre //##DISPLAY_BEGIN## et //##DISPLAY_END##.</p>",
  "validator_code": "<p>Classe Validator avec quatre méthodes de validation indépendantes.</p>",
  "validator_methods": [
    ["validator1", "Titre validation 1", 25],
    ["validator2", "Titre validation 2", 25],
    ["validator3", "Titre validation 3", 25],
    ["validator4", "Titre validation 4", 25]
  ],
  "main_code": "<p>Classe Main appelant toutes les méthodes de Validator.</p>",
  "possible_solution": "<p>Solution correcte de l’exercice.</p>",
  "category": "{category}",
  "difficulty": "{difficulty}",
  "time_limit": 1200,
  "score": 100,
  "tags": {tags},
  "programming_language": "java"
}}

Contraintes supplémentaires (à respecter dans les valeurs) :
- `programming_language` = "java".
- `time_limit` selon `difficulty` : EASY ∈ [600,1200], MEDIUM ∈ [1200,1800], HARD ∈ [1800,2400].
- `score` selon `difficulty` : EASY=100, MEDIUM=200, HARD=300.
- Les 4 méthodes de `validator_methods` doivent correspondre exactement aux 4 méthodes présentes dans `validator_code`.
- La somme des points dans `validator_methods` = `score`.
"""
    return prompt_system.strip(), prompt_user.strip()
