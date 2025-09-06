"""
Module: ai_exam_generator/freeform_choice_exam_generator.py

Generates batches of exam questions via a RAG pipeline (FAISS + LLM):
- Freeform (short answer)
- Choice (QCU/QCM)

Uses semantic context retrieval from FAISS and 40% AI-generated content per type.
"""

from ..ai_question_generator.context import retrieve_context
from ..ai_question_generator.generators.freeform_generator import generate_freeform_question
from ..ai_question_generator.generators.choice_generator import generate_choice_question
from langchain_community.vectorstores import FAISS
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


def freeform_exam_generator(generate_exam: Dict[str, Any], difficulty: str, category: str, vectorstore: FAISS):
    """
    Generate freeform (short answer) questions using FAISS context and LLM.

    ~40% of the requested `freeQuestion` count is generated via AI for each tag.

    Args:
        generate_exam: List of configs with tags and counts.
        difficulty: "EASY", "MEDIUM", or "HARD".
        category: Question category (e.g., backend).
        vectorstore: FAISS store for semantic context retrieval.

    Returns:
        List of JSON-formatted freeform questions.
    """
    ai_freeform_questions = []

    for exam_config in generate_exam:
        tag = exam_config["tag"]
        # Determine number of AI-generated freeform questions (40% of total requested)
        nb_freeform_ai = int(exam_config['freeQuestion'] * 0.4)

        # Retrieve context based on the first tag (e.g., "java", "sql", etc.)
        context = retrieve_context(tag[0], vectorstore)
        print(context)
        for _ in range(nb_freeform_ai):
            try:
                question = generate_freeform_question(category=category, difficulty=difficulty, tags=tag, context=context)
                if question:
                    ai_freeform_questions.append(question)
                    logger.info("Generated freeform question for tag: %s", tag)
            except Exception as e:
                logger.error("Failed to generate freeform question for tag %s: %s", tag, str(e))

    logger.info("Generated %d AI freeform questions total", len(ai_freeform_questions))
    return ai_freeform_questions


def choice_exam_generator(generate_exam: Dict[str, Any], difficulty: str, category: str, vectorstore: FAISS):
    """
    Generate choice (QCU/QCM) questions using FAISS context and LLM.

    ~40% of the requested `questionChoice` count is generated via AI for each tag.

    Args:
        generate_exam: List of configs with tags and counts.
        difficulty: "EASY", "MEDIUM", or "HARD".
        category: Question category (e.g., backend).
        vectorstore: FAISS store for semantic context retrieval.

    Returns:
        List of JSON-formatted choice questions.
    """
    ai_choice_questions = []

    for exam_config in generate_exam:
        tag = exam_config["tag"]
        # Determine number of AI-generated choice questions (40% of total requested)
        nb_choice_ai = int(exam_config["questionChoice"] * 0.4)

        # Retrieve context based on the first tag
        context = retrieve_context(tag[0], vectorstore)

        for _ in range(nb_choice_ai):
            try:
                question = generate_choice_question(category=category, difficulty=difficulty, tags=tag, qtype='QCU', context=context)
                if question:
                    ai_choice_questions.append(question)
                    logger.info("Generated choice question for tag: %s", tag)
            except Exception as e:
                logger.error("Failed to generate choice question for tag %s: %s", tag, str(e))

    logger.info("Generated %d AI choice questions total", len(ai_choice_questions))
    return ai_choice_questions
