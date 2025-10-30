from sentence_transformers import SentenceTransformer
import numpy as np
from functools import lru_cache
from app.core.config import settings

@lru_cache(maxsize=1)
def _model():
    return SentenceTransformer(settings.EMBEDDING_MODEL)

def embed_text(text: str):
    vec = _model().encode(text, convert_to_tensor=False)
    import numpy as np
    vec = np.asarray(vec, dtype=float)
    n = np.linalg.norm(vec) + 1e-10
    return (vec / n).tolist()

def make_search_doc(pet: dict) -> str:
    parts = [
        pet.get("name",""),
        pet.get("breed",""),
        " ".join(pet.get("tags", []) or []),
        pet.get("description",""),
    ]
    return " ".join(p.strip() for p in parts if p)
