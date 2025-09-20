import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def compute_semantic_similarity(str1, str2):
    ea = np.array(emb.embed_query(str1))
    eb = np.array(emb.embed_query(str2))
    return abs(cosine(ea, eb))


def cosine(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return float(np.dot(a, b))
