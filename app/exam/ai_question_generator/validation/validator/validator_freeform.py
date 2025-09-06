"""
Module: validation/validator/validator_freeform.py

Validates "freeform" question payloads against the defined JSON Schema.
"""

import jsonschema
from ..schema import QUESTION_FREEFORM_SCHEMA

def validate_freeform_payload(payload: dict) -> dict:
    """
    Validate a freeform question payload.

    Args:
        payload (dict): The question data to validate.

    Raises:
        jsonschema.ValidationError: If the payload does not match the schema.

    Returns:
        dict: The validated payload.
    """
    jsonschema.validate(payload, QUESTION_FREEFORM_SCHEMA)
    return payload
