#Might need to cheat with a gamestate: https://joelgrus.com/2020/10/02/creating-games-in-streamlit/
#Use this as refernce when you want to build a learning module
import streamlit as st
import chess, chess.pgn, chess.svg
import base64
import random
import dataclasses
import time

from chessboard import display
from custom_classes import Classboard
from game_state import persistent_game_state
from custom_functions import render_svg
from pathlib import Path

p = Path('.')
opening_file_path = p / 'openings'
# for file_name in new_file_path.iterdir():
#     st.write(str(file_name)) 

openings_list = [str(file_name).replace('openings/', "") for file_name in opening_file_path.iterdir()]
opening_choice = st.selectbox('Choose your opening', openings_list)

variation_file_path = opening_file_path / opening_choice
variation_list = [str(file_name).replace('openings/' + opening_choice + '/', "") for file_name in variation_file_path.iterdir()]
cleaned_variation_list = [v.replace('.pgn', "") for v in variation_list]
variation_choice = st.selectbox('Choose your variation', cleaned_variation_list)

user_variation_decision = p / opening_file_path/ opening_choice / variation_choice

user_opening_variation_choice = open(str(user_variation_decision) + ".pgn")

# st.write(user_opening_variation_choice)


#Turning chess 
correct_open_variation = chess.pgn.read_game(user_opening_variation_choice)
# play_mode = st.checkbox("check to start game, then submit first move")

@dataclasses.dataclass
class GameState:
    number: int
    num_guesses: int = 0
    game_number: int = 0
    game_over: bool = True


state = persistent_game_state(initial_state=GameState(random.randint(1, 1000)))

if st.button("NEW GAME"):
    state.number = random.randint(1, 1000)
    state.move_index = 0
    state.game_number += 1
    state.game_over = False
    state.correct_moves = [move for move in correct_open_variation.mainline_moves()]
    state.board = correct_open_variation.board()
    
# st.write(state.correct_moves)

if not state.game_over:
    user_move = st.text_input(f"Enter your chess move in the following format (a1h8)", value="a1h8", key=state.game_number)
    submit_answer = st.button("Submit Answer")
    try:
        if user_move == str(state.correct_moves[state.move_index]) and submit_answer:
        #If the user move equals the stringified correct move, then move the chess pieces twice (once for the user, once for the computer response) and continue on with the game
            state.board.push(state.correct_moves[state.move_index]) #user move
            state.move_index += 1
            with st.spinner('Computer thinking of response, please wait'):
                time.sleep(5)
            state.board.push(state.correct_moves[state.move_index]) #correct computer response
            state.move_index += 1
            st.write("Correct! you have made the right move. Your opponent has responded. Can you keep on going?")
            st.write(state.correct_moves[state.move_index]) #Delete this later, but keep for testing
            # render_svg(chess.svg.board(state.board))
        elif chess.Move.from_uci(user_move) in state.board.legal_moves and user_move != str(state.correct_moves[state.move_index]) and submit_answer:
            state.game_over = True
            st.warning(f"Unfortunately you did not make the correct move. You selected {user_move} but the correct move is {state.correct_moves[state.move_index]}. To restart press New Game")
        elif user_move not in state.board.legal_moves and submit_answer: 
            st.warning("Im sorry but your move didn't register. Please make sure that you include both moves together without spaces in the following format (a1h8)")
    except AttributeError:
        st.write("This is an attribute error")
        st.write("Select New Game to begin")        
        # st.image("./white_start.png")
    except IndexError:
        state.game_over = True
        st.balloons()
        st.success("Congratulations, You have successfully completed the variationl, press New Game to begin again")
        
    render_svg(chess.svg.board(state.board))