import streamlit as st
import random
from logic import Wuzzle

# Initialize game and session state
if 'game' not in st.session_state:
    st.session_state.game = Wuzzle("RAYAN")

if 'guess_history' not in st.session_state:
    st.session_state.guess_history = []

if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# Function to reset the game
def restart_game():
    # You could use a list of words and select randomly
    word_list = ["RAYAN", "HELLO", "WORLD", "GAMES", "BOARD", "HOUSE", "LIGHT", "WATER"]
    new_word = random.choice(word_list)
    st.session_state.game = Wuzzle(new_word)
    st.session_state.guess_history = []
    st.session_state.game_over = False

# Title
st.title("🟨🟩 Word Guessing Game (Wuzzle)")

# Input field
guess_input = st.text_input("Enter your guess (5-letter word):", max_chars=5, disabled=st.session_state.game_over)

# On submit
if st.button("Submit Guess", disabled=st.session_state.game_over):
    if len(guess_input) != st.session_state.game.max_word_length:
        st.warning(f"Guess must be exactly {st.session_state.game.max_word_length} letters.")
    elif not st.session_state.game.can_attempt():
        st.warning("No attempts remaining or game already solved!")
    else:
        st.session_state.game.attempt(guess_input)
        result = st.session_state.game.guess(guess_input.upper())  # Make uppercase if needed

        result_line = ""
        for letter in result:
            color = "🟩" if letter.in_position else "🟨" if letter.in_word else "⬜"
            result_line += f"{color} {letter.character.upper()} "

        st.session_state.guess_history.append(result_line)  # Save formatted result line

        # Check for win/loss
        if st.session_state.game.is_solved():
            st.balloons()
            st.success("🎉 Correct! You've solved the puzzle!")
            st.session_state.game_over = True
        elif not st.session_state.game.can_attempt():
            st.error(f"Game Over! The word was {st.session_state.game.secret}")
            st.session_state.game_over = True

# Show replay button when game is over
if st.session_state.game_over:
    if st.button("Play Again"):
        restart_game()
        st.rerun() 

# Show previous guesses
st.subheader("Your Guesses:")
for line in st.session_state.guess_history:
    st.write(line)

# Show remaining attempts and guesses
st.markdown(f"**Attempts Remaining:** {st.session_state.game.remaining_attempts()}")
st.markdown(f"**Attempts Made:** {', '.join(st.session_state.game.attempts)}")