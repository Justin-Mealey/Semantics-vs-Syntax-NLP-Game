import math
import random

import streamlit as st

from constants import prompts
from semantics import compute_semantic_similarity
from syntax import compute_syntactic_similarity

st.set_page_config(
    page_title="Syntax vs Semantics Game",
    page_icon=":signal_strength:",
    layout="centered",
)

if "score" not in st.session_state:
    st.session_state.score = 0

if "prompt" not in st.session_state:
    st.session_state.prompt = random.choice(prompts)

if "last_turn_status_message" not in st.session_state:
    st.session_state.last_turn_status_message = ""

# PAGE CONTENT START
st.title("Syntax vs Semantics Game")
st.write("Write a sentence that is **semantically** very similar, but **syntactically** very different.")

with st.container(horizontal_alignment="center"):
    st.subheader(f"Current Score: {st.session_state.score}", divider="blue")
    st.write(st.session_state.get("last_turn_status_message"))
    st.write(st.session_state.prompt)

    with st.form(key="response_form"):
        response = st.text_input(label="Enter your sentence")
        submitted = st.form_submit_button("Submit")

        if submitted and response and response.strip():
            prompt = st.session_state.prompt
            semantic_score = math.trunc(compute_semantic_similarity(prompt, response) * 100)
            syntax_score = math.trunc(compute_syntactic_similarity(prompt, response) * 100)

            status_message = (
                f"Your semantic score for the last response was {semantic_score}, and your syntax score"
                f" was {syntax_score}, so {semantic_score - syntax_score} was added to your total score."
            )

            st.session_state.score += semantic_score - syntax_score
            st.session_state.prompt = random.choice(prompts)
            st.session_state.last_turn_status_message = status_message

            st.rerun()
