"""
Module: faiss/build_vectorstore.py

Builds a FAISS vector index from a dataset of exam questions stored in a CSV file.
"""

import os
# ---- IMPORTANT : forcer le CPU avant imports torch/sentence-transformers
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import re
import logging
import pandas as pd
from pandas import DataFrame

from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
# (Optionnel) si tu veux choisir explicitement COSINE selon ta version :
# from langchain_core.vectorstores import DistanceStrategy

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def remove_img_tags(html: str) -> str:
    """Remove all <img> tags from an HTML string."""
    return re.sub(r"<img[^>]*>", "", html or "")


def build_vectorstore(df: DataFrame, output_dir: str = "faiss_index") -> FAISS:
    """
    Build and save a FAISS vector index from a dataset of exam questions.
    """
    documents = []
    for _, row in df.iterrows():
        statement = remove_img_tags(str(row.get("statement", "")))
        metadata = {
            "statement": statement,
            "question_type": row.get("question_type"),
            "category": row.get("category"),
            "difficulty": row.get("difficulty"),
            "exact_response": row.get("exact_response"),
            "tags": row.get("tags"),
            "hint": row.get("hint"),
            "help_description": row.get("help_description"),
            "time_limit": row.get("time_limit"),
            "validation_type": row.get("validation_type"),
            "validator_code": row.get("validator_code"),
            "main_code": row.get("main_code"),
            "programming_language": row.get("programming_language"),
            "initial_candidate_code": row.get("initial_candidate_code"),
            "initial_candidate_test_code": row.get("initial_candidate_test_code"),
            "possible_solution": row.get("possible_solution"),
            "score": row.get("score"),
            "type": row.get("type"),
        }
        documents.append(Document(page_content=statement, metadata=metadata))

    # Embeddings HF (MiniLM-L6-v2), CPU, normalisation -> cosinus
    emb = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    # FAISS vectorstore
    # Si ta version supporte la stratégie :
    # vectorstore = FAISS.from_documents(
    #     documents, emb, distance_strategy=DistanceStrategy.COSINE
    # )
    vectorstore = FAISS.from_documents(documents, emb)
    vectorstore.save_local(output_dir)
    logger.info("FAISS vectorstore saved in: %s", output_dir)
    return vectorstore


if __name__ == "__main__":
    # Charger les questions depuis le fichier CSV
    df = pd.read_csv("./data/questions.csv")
    print(df.head())

    # Construire et sauvegarder l'index FAISS
    build_vectorstore(df)
