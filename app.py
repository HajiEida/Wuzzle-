import streamlit as st
from logic import Wuzzle

# Session state
if 'game' not in st.session_state:
    st.session_state.game = Wuzzle("RAYAN")
if 'message' not in st.session_state:
    st.session_state.message = ""

st.title("🟨🟩 Word Guessing Game (Wuzzle)")

guess_input = st.text_input("Enter your guess (5-letter word):", max_chars=5)

if st.button("Submit Guess"):
    if len(guess_input) != st.session_state.game.max_word_length:
        st.warning(f"Guess must be exactly {st.session_state.game.max_word_length} letters.")
    elif not st.session_state.game.can_attempt():
        st.warning("No attempts remaining or game already solved!")
    else:
        st.session_state.game.attempt(guess_input)
        result = st.session_state.game.guess(guess_input)

        for letter in result:
            color = "🟩" if letter.in_position else "🟨" if letter.in_word else "⬜"
            st.write(f"{color} {letter.character}")

        if st.session_state.game.is_solved():
            st.balloons()
            st.success("🎉 Correct! You've solved the puzzle!")
        elif not st.session_state.game.can_attempt():
            st.error(f"Game Over! The word was {st.session_state.game.secret}")

st.markdown(f"**Attempts Remaining:** {st.session_state.game.remaining_attempts()}")
st.markdown(f"**Attempts Made:** {', '.join(st.session_state.game.attempts)}")
