import streamlit as st

from compare import semantic_sim


def instructions_page():
    st.title("Instructions")

    st.write("""
    Welcome to the Semantics vs Syntax NLP Game!

    This is a game where you can explore how sentences can be rewritten
    while preserving their meaning but changing their structure.

    Click the button below to start the game.
    """)

    if st.button("Start Game", type="primary"):
        st.session_state.page = "game"
        st.rerun()


def game_page():
    st.title("Basic Streamlit App")

    # Display the sentence we are comparing to
    st.subheader("Sentence to compare:")
    reference_sentence = "The cat sat on the mat."
    st.write(f"**{reference_sentence}**")

    st.divider()

    # Input window
    user_input = st.text_input("Enter your text here:")

    # Display the input below and calculate semantic similarity
    if user_input:
        st.write("You entered:")
        st.write(user_input)

        # Calculate and display semantic similarity score
        try:
            with st.spinner("Calculating semantic similarity..."):
                similarity_score = semantic_sim(reference_sentence, user_input)

            st.subheader("Semantic Similarity Score:")
            st.metric(
                label="Similarity",
                value=f"{similarity_score:.3f}",
                help="Score ranges from 0 (completely different) to 1 (identical meaning)",
            )

            # Add interpretation
            if similarity_score >= 0.80:
                st.success(
                    "🎉 Great! High semantic similarity - meanings are very close!"
                )
            elif similarity_score >= 0.60:
                st.warning(
                    "⚠️ Moderate semantic similarity - meanings are somewhat related."
                )
            else:
                st.error("❌ Low semantic similarity - meanings are quite different.")

        except Exception as e:
            st.error(f"Error calculating similarity: {e}")

    # Button to go back to instructions
    if st.button("Back to Instructions"):
        st.session_state.page = "instructions"
        st.rerun()


def main():
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "instructions"

    # Route to appropriate page
    if st.session_state.page == "instructions":
        instructions_page()
    elif st.session_state.page == "game":
        game_page()


if __name__ == "__main__":
    main()
