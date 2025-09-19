import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# or: "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# or an API embedding like OpenAI via langchain-openai's OpenAIEmbeddings


def cosine(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return float(np.dot(a, b))


def semantic_sim(a: str, b: str) -> float:
    ea = np.array(emb.embed_query(a))
    eb = np.array(emb.embed_query(b))
    return cosine(ea, eb)


def are_semantically_similar(a: str, b: str, threshold: float = 0.80) -> bool:
    return semantic_sim(a, b) >= threshold


# s1 = "The cat sat on the mat."
# s2 = "A cat was sitting on the rug."
# score = semantic_sim(s1, s2)
# print(score, "-> similar?", score >= 0.80)
