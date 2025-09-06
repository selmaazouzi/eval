from pathlib import Path

def get_faiss_index_path():
    return Path(__file__).parent / "faiss_index"
