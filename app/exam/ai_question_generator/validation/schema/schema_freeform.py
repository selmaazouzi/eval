"""
Module: validation/schema/schema_freeform.py

Defines the JSON Schema for validating freeform (short-answer) questions.

Main Responsibilities:
- Ensure generated JSON strictly matches the expected structure.
- Allow `tags` to be provided as either a string or an array of strings.
- Enforce field requirements, types, and constraints.
"""

TAGS_STRING_OR_ARRAY = {
    "anyOf": [
        {"type": "string", "minLength": 1},
        {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 1}
    ]
}

QUESTION_FREEFORM_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "question_type", "statement", "category", "difficulty",
        "score", "time_limit", "tags", "help_description",
        "validation_type", "exact_response"
    ],
    "properties": {
        "question_type": {"type": "string", "const": "freeform"},
        "statement": {"type": "string", "minLength": 5},
        "category": {"type": "string", "minLength": 2},
        "difficulty": {"type": "string", "enum": ["EASY", "MEDIUM", "HARD"]},
        "score": {"type": "integer"},
        "time_limit": {"type": "integer"},
        "tags": TAGS_STRING_OR_ARRAY,
        "help_description": {"type": "string", "minLength": 3},
        "validation_type": {"type": "string", "const": "Exact_Match"},
        "exact_response": {"type": "string", "minLength": 3}
    }
}
