"""
Module: validation/schema/schema_choice.py 

Defines the JSON Schema for validating multiple-choice questions (QCU or QCM).

Main Responsibilities:
- Ensure generated JSON strictly matches the expected MCQ structure.
- Allow `tags` to be provided as either a string or a list of strings.
- Enforce proper typing and constraints for all fields.
"""

TAGS_STRING_OR_ARRAY = {
    "anyOf": [
        {"type": "string", "minLength": 1},
        {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 1}
    ]
}

QUESTION_CHOICE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "question_type","statement","category","difficulty",
        "score","time_limit","tags","help_description",
        "type","answers","right_answer"
    ],
    "properties": {
        "question_type": {"type": "string", "const": "choice"},
        "statement": {"type": "string", "minLength": 5},
        "category": {"type": "string", "minLength": 2},
        "difficulty": {"type": "string", "enum": ["EASY","MEDIUM","HARD"]},
        "score": {"type": "integer"},
        "time_limit": {"type": "integer"},
        "tags": TAGS_STRING_OR_ARRAY,
        "help_description": {"type": "string", "minLength": 3},
        "type": {"type": "string", "enum": ["QCM","QCU"]},
        "answers": {
            "type": "array",
            "minItems": 2,
            "items": {"type": "string", "minLength": 1}
        },
        # right_answer peut être une string (QCU) OU une liste de strings (QCM)
        "right_answer": {
            "anyOf": [
                {"type": "string", "minLength": 1},
                {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}}
            ]
        }
    }
}
