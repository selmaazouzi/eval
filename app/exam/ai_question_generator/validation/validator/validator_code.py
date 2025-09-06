"""
Module: validator/validator_code.py

Validates "code" question payloads against the defined JSON schema.
"""

from __future__ import annotations
import jsonschema
from ..schema.schema_code import QUESTION_CODE_SCHEMA


def validate_code_payload(payload: dict) -> dict:
    """
    Validate a code question payload.

    Checks:
    - JSON Schema compliance.

    Args:
        payload (dict): The question data.

    Raises:
        jsonschema.ValidationError: If schema is invalid.
        
    Returns:
        dict: The validated payload.
    """
    jsonschema.validate(payload, QUESTION_CODE_SCHEMA)
    return payload
