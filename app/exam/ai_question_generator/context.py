"""
Module: ai_question_generator/context.py

Provides utilities for retrieving and formatting example questions from the FAISS vector store
to be used as few-shot context in a Retrieval-Augmented Generation (RAG) pipeline.

Main Responsibilities:
- Search the vector database for the most similar existing questions.
- Format retrieved metadata into JSON-like examples suitable for prompt injection.

Functions:
- retrieve_context(query, vectordb, k): Performs a similarity search and returns formatted examples.
- generate_context_snippet(docs): Converts retrieved documents into filtered JSON snippets
  based on their question type.
"""

import json

# Définir les champs à inclure par type de question
TYPE_FIELDS_MAP = {
    "freeform": [
        "statement", "question_type", "category", "difficulty", "tags",
        "score", "time_limit", "help_description", "hint",
        "validation_type", "exact_response"
    ],
    "choice": [
        "statement", "question_type", "category", "difficulty", "tags",
        "score", "time_limit", "help_description", "hint",
        "answers", "choice_type"
    ],
    "code": [
        "statement", "question_type", "category", "difficulty", "tags",
        "score", "time_limit", "help_description", "hint",
        "initial_candidate_code", "initial_candidate_test_code",
        "validator_code", "main_code", "programming_language"
    ]
}

def generate_context_snippet(docs):
    """
    Formats the metadata of retrieved documents into a JSON-like string block.

    Args:
        docs (List[Document]): A list of LangChain Document objects returned by FAISS.

    Returns:
        str: A concatenated string of example questions in JSON format, separated by delimiters.
    """
    examples = []
    for doc in docs:
        meta = doc.metadata
        snippet = {
            "statement": meta.get("statement"),
            "question_type": meta.get("question_type"),
            "category": meta.get("category"),
            "difficulty": meta.get("difficulty"),
            "tags": meta.get("tags"),
            "score": meta.get("score"),
            "time_limit": meta.get("time_limit"),
            "help_description": meta.get("help_description"),
            "hint": meta.get("hint"),
            "validation_type": meta.get("validation_type"),
            "exact_response": meta.get("exact_response")
        }
        examples.append(snippet)

    # Return all examples as formatted JSON strings, separated by ---
    return "\n---\n".join([json.dumps(e, ensure_ascii=False, indent=2) for e in examples])

def retrieve_context(query, vectordb, k=5):
    """
    Searches the vector database for top-k most relevant documents.

    Args:
        query (str): The user's query or topic of interest.
        vectordb (FAISS): The vector store instance to search.
        k (int): The number of top results to return (default is 5).

    Returns:
        str: A formatted context string built from the top-k matched documents.
    """
    docs = vectordb.similarity_search(query, k=k)
    return generate_context_snippet(docs)
