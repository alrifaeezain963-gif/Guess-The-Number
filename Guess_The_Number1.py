import streamlit as st
import random

st.set_page_config(page_title="Guess The Number", page_icon="🎮", layout="centered")

st.title("🎮 Guess The Number Game")

if 'secret_number' not in st.session_state:
    st.session_state.secret_number = None
if 'max_tries' not in st.session_state:
    st.session_state.max_tries = 0
if 'counter' not in st.session_state:
    st.session_state.counter = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'feedback_history' not in st.session_state:
    st.session_state.feedback_history = []
if 'max_value' not in st.session_state:
    st.session_state.max_value = 100

def start_game(level):
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.counter = 0
    st.session_state.feedback_history = []
    
    if level == 1:
        st.session_state.max_value = 50
        st.session_state.max_tries = 5
        st.session_state.secret_number = random.randint(1, 50)
    elif level == 2:
        st.session_state.max_value = 100
        st.session_state.max_tries = 7
        st.session_state.secret_number = random.randint(1, 100)
    elif level == 3:
        st.session_state.max_value = 200
        st.session_state.max_tries = 10
        st.session_state.secret_number = random.randint(1, 200)

if not st.session_state.game_started:
    st.write("Welcome to guess the number game, there are 3 different difficulty levels:")
    st.write("* **First (1) is easy** where the computer will choose number between 1 and 50 (5 tries)")
    st.write("* **Second (2) is normal** where the computer will choose number between 1 and 100 (7 tries)")
    st.write("* **Third (3) is difficult** where the computer will choose number between 1 and 200 (10 tries)")
    
    level_choice = st.selectbox("Enter your choice (1, 2, 3) :", options=[1, 2, 3], index=0)
    if st.button("🚀 Start Game"):
        start_game(level_choice)
        st.rerun()

else:
    st.write(f"Can you guess the number i chose between 1 and {st.session_state.max_value}, but you only have {st.session_state.max_tries} tries.")
    st.info(f"Tries used: {st.session_state.counter} / {st.session_state.max_tries}")
    
    for feed in st.session_state.feedback_history:
        if "correct" in feed or "Congrats" in feed:
            st.success(feed)
        elif "lost" in feed or "Cold" in feed:
            st.error(feed)
        else:
            st.warning(feed)

    if not st.session_state.game_over:
        user_guess = st.number_input("enter your guess: ", min_value=1, max_value=st.session_state.max_value, step=1, key="user_guess_input")
        
        if st.button("🎯 Submit Guess"):
            accuracy = abs(user_guess - st.session_state.secret_number)
            
            if accuracy == 0:
                st.session_state.feedback_history.append("your guess is correct")
                st.session_state.feedback_history.append("Congrats you won")
                st.session_state.game_over = True
                st.balloons()
            else:
                st.session_state.counter += 1
                if accuracy > 3:
                    st.session_state.feedback_history.append(f"Guess {user_guess}: Cold")
                else:
                    st.session_state.feedback_history.append(f"Guess {user_guess}: Hot")
                
                if st.session_state.counter == st.session_state.max_tries:
                    st.session_state.feedback_history.append("You lost :(")
                    st.session_state.feedback_history.append(f"The number was: {st.session_state.secret_number}")
                    st.session_state.game_over = True
            st.rerun()

    if st.session_state.game_over:
        st.write("Do you want to play again?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🟢 Yes"):
                st.session_state.game_started = False
                st.session_state.game_over = False
                st.rerun()
        with col2:
            if st.button("🔴 No"):
                st.write("Thanks for playing! 👋")