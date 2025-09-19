import random

import streamlit as st

from semantics import compute_semantic_similarity
from syntax import compute_syntactic_similarity

st.set_page_config(
    page_title="Syntax vs Semantics Game", page_icon="📝", layout="centered"
)

st.title("Syntax vs Semantics Game")
st.subheader(
    "Write a sentence that is **semantically** very similar, "
    "but **syntactically** very different."
)

if "score" not in st.session_state:
    st.session_state.score = 0

example_sentences = [
    "The happy child played with the sad puppy in the park.",
    "She ran quickly while he walks slowly down the street.",
    "The king and queen ruled their kingdom with wisdom.",
]


with st.container(horizontal_alignment="center"):
    st.subheader(f"Current Score: {st.session_state.get('score', 0)}", divider="grey")

    prompt = random.choice(example_sentences)
    st.write(prompt)

    response = st.text_input(label="Your sentence")

    if response is not None:
        semantic_score = compute_semantic_similarity(prompt, response)
        syntax_score = compute_syntactic_similarity(prompt, response)

        st.session_state["score"] += semantic_score - syntax_score
