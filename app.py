import streamlit as st
from logic import Wuzzle
from word_generator import WordGenerator
from ai_solver import AISolver

if 'word_generator' not in st.session_state:
    st.session_state.word_generator=WordGenerator()

if 'ai_solver' not in st.session_state:
    st.session_state.ai_solver=AISolver(st.session_state.word_generator.valid_words)

if 'game' not in st.session_state:
    new_word=st.session_state.word_generator.generate_word()
    st.session_state.game=Wuzzle(new_word)

if 'guess_history' not in st.session_state:
    st.session_state.guess_history=[]

if 'game_over' not in st.session_state:
    st.session_state.game_over=False

def restart_game():
    new_word=st.session_state.word_generator.generate_word()
    st.session_state.game=Wuzzle(new_word)
    st.session_state.guess_history=[]
    st.session_state.game_over=False

st.title("🟨🟩 Word Guessing Game (Wuzzle)")

with st.expander("📋 Game Rules"):
    st.markdown("""
    ### How to Play Wuzzle:
    
    1. **Objective:** Guess the secret 5-letter word within 6 attempts.
    
    2. **Making a Guess:** Enter a valid 5-letter word and submit your guess.
    
    3. **Feedback:**
       - 🟩 Green: Letter is correct and in the right position
       - 🟨 Yellow: Letter is in the word but in the wrong position
       - ⬜ Gray: Letter is not in the word
    
    4. **Strategy:** Use the feedback from previous guesses to narrow down possibilities.
    
    5. **Winning:** Guess the correct word within 6 attempts to win!
    
    6. **Losing:** If you don't guess the word within 6 attempts, the game is over and the secret word will be revealed.
    """)

guess_input=st.text_input(
    "Enter your guess (5-letter word):",
    max_chars=5,
    disabled=st.session_state.game_over,
    key='guess_input'
)

if st.button("Submit Guess", disabled=st.session_state.game_over):
    if len(guess_input) != st.session_state.game.max_word_length:
        st.warning(f"Guess must be exactly {st.session_state.game.max_word_length} letters.")
    elif not st.session_state.game.can_attempt():
        st.warning("No attempts remaining or game already solved!")
    else:
        st.session_state.game.attempt(guess_input)
        result=st.session_state.game.guess(guess_input.upper())

        result_line=""
        for letter in result:
            color="🟩" if letter.in_position else "🟨" if letter.in_word else "⬜"
            result_line += f"{color} {letter.character.upper()} "

        st.session_state.guess_history.append(result_line)

        if st.session_state.game.is_solved():
            st.balloons()
            st.success("🎉 Correct! You've solved the puzzle!")
            st.session_state.game_over=True
        elif not st.session_state.game.can_attempt():
            st.error(f"Game Over! The word was {st.session_state.game.secret}")
            st.session_state.game_over=True 

if st.session_state.game_over:
    if st.button("Play Again"):
        restart_game()
        st.rerun()

st.subheader("Your Guesses:")
for line in st.session_state.guess_history:
    st.write(line)

st.markdown(f"**Attempts Remaining:** {st.session_state.game.remaining_attempts()}")
st.markdown(f"**Attempts Made:** {', '.join(st.session_state.game.attempts)}")

st.divider()
st.header("🧠 AI Solver Lab")

target_word=st.text_input(
    "Enter a 5-letter word for the AI to solve:",
    max_chars=5,
    key='target_word'
)

if st.button("Run AI Solver"):
    if len(target_word) != 5:
        st.warning("Please enter exactly 5 letters")
    else:
        st.session_state.ai_solver.reset()
        solution=st.session_state.ai_solver.solve(target_word.upper())
        
        st.subheader(f"🧠 AI Solution for: {target_word.upper()}")
        
        for i, step in enumerate(solution, 1):
            with st.expander(f"Move {i}: {step['guess']}", expanded=i==1):
                cols=st.columns(2)
                cols[0].metric("Possible Words Remaining", step['remaining'])
                
                explanation_lines=step['explanation'].split('\n')
                for line in explanation_lines:
                    if line.startswith("🎯"):
                        st.success(line)
                    elif line.startswith("📊"):
                        st.markdown(f"**{line}**")
                    elif line.startswith("🏆"):
                        st.markdown(f"**{line}**")
                    elif line.startswith(("1.", "2.", "3.")):
                        parts=line.split("(")
                        st.markdown(f"**{parts[0]}**")
                        st.caption(parts[1].replace(")", ""))
                    elif ":" in line and not line.startswith(" "):
                        key, value=line.split(":", 1)
                        st.markdown(f"**{key}:** {value}")
                    else:
                        st.write(line)
                
                if step['guess'] == target_word.upper():
                    st.balloons()
                    st.success(f"✅ Solved in {i} moves!")