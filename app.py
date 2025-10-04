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

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0

if "score_history" not in st.session_state:
    st.session_state.score_history = []

if "detailed_score_history" not in st.session_state:
    st.session_state.detailed_score_history = []

if "prompt" not in st.session_state:
    st.session_state.prompt = random.choice(prompts)

if "page" not in st.session_state:
    st.session_state.page = "game"  # "game" or "score_explanation"

if "last_semantic_score" not in st.session_state:
    st.session_state.last_semantic_score = 0

if "last_syntax_score" not in st.session_state:
    st.session_state.last_syntax_score = 0

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""


def show_score_history_table():
    """Helper function to display the score history table"""
    if len(st.session_state.detailed_score_history) > 0:
        st.subheader("Your Recent Performance", divider="gray")

        # Get last 5 rounds for the table
        recent_rounds = st.session_state.detailed_score_history[-5:]

        # Display as columns without table lines
        col_headers = st.columns([1, 2, 2, 2])
        with col_headers[0]:
            st.write("**Round**")
        with col_headers[1]:
            st.write("**Semantic**")
        with col_headers[2]:
            st.write("**Syntax**")
        with col_headers[3]:
            st.write("**Points**")

        # Display each round's data
        start_round = len(st.session_state.detailed_score_history) - len(recent_rounds) + 1
        for i, round_data in enumerate(recent_rounds):
            cols = st.columns([1, 2, 2, 2])
            with cols[0]:
                st.write(f"{start_round + i}")
            with cols[1]:
                st.write(f"{round_data['semantic']}%")
            with cols[2]:
                st.write(f"{round_data['syntax']}%")
            with cols[3]:
                points = round_data["semantic"] - round_data["syntax"]
                if points > 0:
                    st.write(f"+{points}")
                else:
                    st.write(f"{points}")

        st.write("")  # Add spacing


def show_game_page():
    """Display the main game page with prompt and input"""
    st.title("Syntax vs Semantics Game")
    st.write("Write a sentence that is **semantically** very similar, but **syntactically** very different.")

    with st.container():
        st.subheader(f"Current Score: {st.session_state.score}", divider="blue")
        st.write("**Your prompt:**")
        st.write(f"*{st.session_state.prompt}*")

        with st.form(key="response_form"):
            response = st.text_input(label="Enter your sentence", key="response_input")
            submitted = st.form_submit_button("Submit")

            if submitted and response and response.strip():
                # Store the current prompt and response for the score page
                st.session_state.last_prompt = st.session_state.prompt
                st.session_state.last_response = response

                # Calculate scores
                semantic_score = compute_semantic_similarity(st.session_state.prompt, response)
                syntax_score = compute_syntactic_similarity(st.session_state.prompt, response)

                # Store scores for the explanation page
                st.session_state.last_semantic_score = math.trunc(semantic_score * 100)
                st.session_state.last_syntax_score = math.trunc(syntax_score * 100)

                # Update total score
                score_change = st.session_state.last_semantic_score - st.session_state.last_syntax_score
                st.session_state.score += score_change

                # Add score change to history (keep only last 5)
                st.session_state.score_history.append(score_change)

                # Add detailed scores to history
                st.session_state.detailed_score_history.append(
                    {"semantic": st.session_state.last_semantic_score, "syntax": st.session_state.last_syntax_score}
                )

                # Generate new prompt for next round
                st.session_state.prompt = random.choice(prompts)

                # Switch to score explanation page
                st.session_state.page = "score_explanation"
                st.rerun()

    # Show score history table at the bottom
    show_score_history_table()


def show_score_explanation_page():
    """Display the score explanation page between prompts"""
    st.title("Score Breakdown")

    # Show the previous prompt and response
    st.subheader("What you just completed:", divider="green")
    st.write("**Prompt:**")
    st.write(f"*{st.session_state.last_prompt}*")
    st.write("**Your Response:**")
    st.write(f"*{st.session_state.last_response}*")

    # Show detailed score breakdown
    st.subheader("Score Analysis:", divider="blue")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Semantic Score",
            value=f"{st.session_state.last_semantic_score}%",
            help="How similar your sentence is in meaning to the prompt",
        )

    with col2:
        st.metric(
            label="Syntax Score",
            value=f"{st.session_state.last_syntax_score}%",
            help="How similar your sentence structure is to the prompt",
        )

    with col3:
        score_change = st.session_state.last_semantic_score - st.session_state.last_syntax_score
        st.metric(label="Points Earned", value=f"{score_change:+d}", help="Semantic Score - Syntax Score")

    # Explanation
    st.write("### Explanation:")
    st.write(f"""
    - **Semantic Score ({st.session_state.last_semantic_score}%)**: Measures how well you preserved the meaning
    - **Syntax Score ({st.session_state.last_syntax_score}%)**: Measures how much you changed the sentence structure
    - **Points Earned**: {st.session_state.last_semantic_score} - {st.session_state.last_syntax_score} = **{score_change:+d} points**

    The goal is to get a high semantic score (keep the meaning) while getting a low syntax score (change the structure)!
    """)

    st.subheader(f"Total Score: {st.session_state.score}", divider="rainbow")

    # Next button
    if st.button("Continue to Next Prompt", type="primary", use_container_width=True):
        st.session_state.page = "game"
        st.rerun()

    # Show score history table at the bottom
    show_score_history_table()


# PAGE ROUTING
if st.session_state.page == "game":
    show_game_page()
elif st.session_state.page == "score_explanation":
    show_score_explanation_page()
