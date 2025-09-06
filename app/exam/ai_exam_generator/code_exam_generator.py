"""
Module: ai_exam_generator/code_exam_generator.py

Generates code-based exam questions using FAISS context and an LLM.
Only ~40% of requested code questions are AI-generated; the rest come from the database.
"""
from ..ai_question_generator.context import retrieve_context
from ..ai_question_generator.generators.code_generator import generate_code_question
from langchain_community.vectorstores import FAISS
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def code_exam_generator(code_params: Dict[str, Any], difficulty: str, category: str, vectorstore: FAISS):
    """
    Generate code questions using FAISS context and an LLM.

    ~40% of the requested `questionCodeCount` is generated via AI for the given programming language.

    Args:
        code_params: Config dict with:
            - programmingLanguage: str
            - questionCodeCount: int
        difficulty: "EASY", "MEDIUM", or "HARD".
        category: Question category (e.g., backend).
        vectorstore: FAISS store for semantic context retrieval.

    Returns:
        List of JSON-formatted code questions.
    """
    ai_code_questions = []

    # Retrieve the programming language for which to generate questions
    language = code_params.get('programmingLanguage')

    # Determine number of code questions to generate (40% of the requested count)
    nb_code_ai = int(code_params.get('questionCodeCount', 0) * 0.4)

    # Retrieve relevant context based on the programming language
    context = retrieve_context(language, vectorstore)

    for _ in range(nb_code_ai):
        try:
            # Generate one code question using the provided context
            question = generate_code_question(category=category, difficulty=difficulty, tags=language, context=context)
            if question:
                ai_code_questions.append(question)
                # For debugging: print the question to the console
                logger.info("Generated code question for language: %s", language)
        except Exception as e:
            # Log any failure during generation
            logger.error("Failed to generate code question for language %s: %s", language, str(e))

    logger.info("Generated %d AI code questions total", len(ai_code_questions))
    return ai_code_questions
