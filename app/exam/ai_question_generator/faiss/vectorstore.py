"""
Module: faiss/vectorstore.py

Load the FAISS vector store for similarity search in the RAG pipeline.
"""

import os
import logging
from pathlib import Path

# IMPORTANT: force CPU before any library tries to init CUDA
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

from . import get_faiss_index_path  # Helper to retrieve FAISS index path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_vectorstore():
    """
    Load a FAISS vector store from disk with MiniLM embeddings (CPU + cosine normalization).

    Returns:
        FAISS: Loaded FAISS vector store.

    Raises:
        FileNotFoundError: if the FAISS index directory is missing.
        RuntimeError: if the index dimension doesn't match the embedding model.
    """
    # 1) Embeddings config (aligné avec la phase de build)
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},  # cosine via IP on unit vectors
    )

    # 2) Path de l'index
    index_path = Path(get_faiss_index_path())
    if not index_path.exists():
        raise FileNotFoundError(f"FAISS index not found at: {index_path}")

    logger.info("Loading FAISS index from: %s", index_path)

    # 3) Chargement (docstore pickle → danger si source non fiable)
    vectordb = FAISS.load_local(
        str(index_path),
        embeddings,
        allow_dangerous_deserialization=True  # OK si fichiers générés par toi et de source sûre
    )

    # 4) Sanity check: dimension embeddings vs index
    try:
        test_vec = embeddings.embed_query("dim-check")
        dim_model = len(test_vec)
        dim_index = vectordb.index.d  # FAISS index dimension
        if dim_model != dim_index:
            raise RuntimeError(
                f"Incompatible index: model dim={dim_model} vs FAISS dim={dim_index}. "
                f"Rebuild the index with the same model ({MODEL_NAME})."
            )
    except Exception as e:
        logger.warning("Could not verify index dimension strictly: %s", e)

    logger.info("FAISS vectorstore loaded (model=%s, dim=%s)", MODEL_NAME, vectordb.index.d)
    return vectordb
