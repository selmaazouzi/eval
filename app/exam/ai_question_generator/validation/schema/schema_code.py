"""
Module: validation/schema/schema_code.py

Defines the JSON Schema for validating coding questions (Java/backend).

Responsibilities:
- Enforce structure and types for code question payloads.
- Allow `tags` as a string or a list of strings.
- Validate `validator_methods` as triplets [name, title, points].
"""

TAGS_STRING_OR_ARRAY = {
    "anyOf": [
        {"type": "string", "minLength": 1},
        {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 1}
    ]
}

QUESTION_CODE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "question_type","statement","initial_candidate_code","initial_candidate_test_code",
        "validator_code","validator_methods","main_code","possible_solution",
        "category","difficulty","time_limit","score","tags","programming_language"
    ],
    "properties": {
        "question_type": {"type": "string", "const": "code"},
        "statement": {"type": "string", "minLength": 5},
        "initial_candidate_code": {"type": "string", "minLength": 5},
        "initial_candidate_test_code": {"type": "string", "minLength": 5},
        "validator_code": {"type": "string", "minLength": 5},

        # validator_methods = 4 sous-tableaux [name, title, points]
        "validator_methods": {
            "type": "array",
            "minItems": 2, "maxItems": 4,
            "items": {
                "type": "array",
                "minItems": 3, "maxItems": 3,
                "items": [
                    {"type": "string", "minLength": 1},  # name
                    {"type": "string", "minLength": 2},  # title
                    {"type": "integer", "minimum": 0}     # points
                ]
            }
        },

        "main_code": {"type": "string", "minLength": 5},
        "possible_solution": {"type": "string", "minLength": 5},
        "category": {"type": "string", "minLength": 2},
        "difficulty": {"type": "string", "enum": ["EASY","MEDIUM","HARD"]},
        "time_limit": {"type": "integer"},
        "score": {"type": "integer"},
        "tags": TAGS_STRING_OR_ARRAY,
        "programming_language": {"type": "string", "minLength": 2}
    }
}
