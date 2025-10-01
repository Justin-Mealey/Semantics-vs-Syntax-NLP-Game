import math

import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def curve_semantic_score(score) -> float:
    return math.sqrt(score)


def compute_semantic_similarity(str1, str2):
    v1 = np.array(embeddings.embed_query(str1))
    v2 = np.array(embeddings.embed_query(str2))

    dot_product = np.dot(v1, v2)
    norms = np.linalg.norm(v1) * np.linalg.norm(v2)

    if norms == 0:
        return 0.0

    raw_score = abs(float(dot_product / norms))
    return curve_semantic_score(raw_score)
