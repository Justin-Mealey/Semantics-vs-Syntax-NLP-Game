import math
import random

import streamlit as st

from semantics import compute_semantic_similarity
from syntax import compute_syntactic_similarity

st.set_page_config(
    page_title="Syntax vs Semantics Game",
    page_icon=":signal_strength:",
    layout="centered",
)

prompts = [
    # Basic actions and emotions
    "The happy child played with the sad puppy in the park.",
    "She ran quickly while he walks slowly down the street.",
    "The king and queen ruled their kingdom with wisdom.",
    # Daily activities
    "The chef prepared a delicious meal in the kitchen.",
    "Students quietly studied their books in the library.",
    "The musician practiced his violin until sunset.",
    "They enjoyed coffee and conversation at the café.",
    # Nature and weather
    "Leaves danced in the autumn breeze yesterday afternoon.",
    "Thunder rolled across dark skies during the storm.",
    "Waves crashed against the rocky shore at sunrise.",
    "Birds sang sweetly in the flowering garden.",
    # Work and achievement
    "The scientist made an important discovery in her laboratory.",
    "The artist painted a beautiful landscape on canvas.",
    "The team celebrated their victory after the game.",
    "An entrepreneur launched her startup last month.",
    # Technology and modern life
    "The programmer solved complex problems with elegant code.",
    "Social media connects people across vast distances instantly.",
    "Electric cars silently cruise through city streets.",
    "Satellites orbit Earth transmitting data continuously.",
    # Abstract concepts
    "Time flows like a river through our memories.",
    "Ideas spread rapidly in the digital age.",
    "Knowledge opens doors to new opportunities.",
    "Dreams inspire people to achieve great things.",
    # Social interactions
    "Friends gathered to celebrate the special occasion.",
    "Teachers guide students toward understanding difficult concepts.",
    "Families share meals and stories around the dinner table.",
    "Neighbors helped each other during the difficult times.",
]

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
