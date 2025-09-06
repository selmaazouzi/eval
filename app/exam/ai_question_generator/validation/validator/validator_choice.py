"""
Module: validation/validator/validator_choice.py

Validates "choice" (MCQ/QCU) question payloads against the schema and answer rules.
"""

from __future__ import annotations
import jsonschema
from typing import List
from ..schema.schema_choice import QUESTION_CHOICE_SCHEMA


def _trim_and_dedupe_answers(answers: List[str]) -> List[str]:
    """
    Remove empty entries and duplicates from answer options.

    Args:
        answers (List[str]): Raw answer options.

    Returns:
        List[str]: Cleaned list with unique non-empty answers.
    """
    seen, out = set(), []
    for a in answers:
        a2 = a.strip()
        if not a2:
            continue
        if a2 not in seen:
            seen.add(a2)
            out.append(a2)
    return out


def validate_choice_payload(payload: dict) -> dict:
    """
    Validate a choice question payload.

    Checks:
    - JSON Schema compliance.
    - At least 2 unique non-empty answers.
    - For QCU: `right_answer` is a string present in answers.
    - For QCM: `right_answer` is a string or list, each present in answers.

    Args:
        payload (dict): The question data.

    Raises:
        jsonschema.ValidationError: If schema is invalid.
        ValueError: If logical rules are violated.

    Returns:
        dict: The validated (and possibly normalized) payload.
    """
    # 1) Schema validation
    jsonschema.validate(payload, QUESTION_CHOICE_SCHEMA)

    # 2) Clean/validate answers
    answers = _trim_and_dedupe_answers(payload["answers"])
    if len(answers) < 2:
        raise ValueError("`answers` must contain at least 2 unique non-empty options.")
    payload["answers"] = answers

    # 3) Validate right_answer by type
    qtype = payload["type"]
    ra = payload["right_answer"]

    if qtype == "QCU":
        if isinstance(ra, list):
            raise ValueError("In QCU, `right_answer` must be a string, not a list.")
        if ra not in answers:
            raise ValueError("In QCU, `right_answer` must be in `answers`.")
    else:  # QCM
        ra_list = [ra] if isinstance(ra, str) else list(ra)
        if not ra_list:
            raise ValueError("In QCM, `right_answer` must contain at least one correct answer.")
        missing = [x for x in ra_list if x not in answers]
        if missing:
            raise ValueError(f"In QCM, the answers {missing} are not listed in `answers`.")
        payload["right_answer"] = ra_list

    return payload
