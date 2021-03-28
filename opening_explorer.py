import streamlit as st
import chess, chess.pgn
import base64
from chessboard import display
from custom_functions import render_svg



#Opening files in PGN (Portable Game Notation) format
pgn_md = open("rl_morphys_defense.pgn")

#Turning chess 
m_defense = chess.pgn.read_game(pgn_md)
board = m_defense.board()
play_mode = st.checkbox("check to start game, then submit first move")
user_move = st.text_input("starting square", "a1h8")
enter_move = st.button("submit move")


if play_mode is False: 
    render_svg(chess.svg.board(board))




# color_choice = st.radio("Which color do you want to practice with", ('Black', 'White') )
# open_choice = st.radio("Which Opening do you want to practice",
#     ('Ruy Lopez (Spanish Opening)', 'English Opening', 'Queen\'s Gambit')
# )
# variation_choice = st.radio(f"Which variation of the {open_choice} do you want to practice?",
#    ('Morphy\'s Defense', 'Another Defense') )


if play_mode is True:
    if enter_move:
    #Change m_defense to the variation choice during a later iteration of the project
        moves = [move for move in m_defense.mainline_moves()]
        
        st.write(f'user move is {type(user_move)}')
        st.write(f'moves[current_move] is {str(moves[current_move])}')
        # st.write(user_move == str(moves[current_move]))
        if user_move == str(moves[current_move]):
            board.push(moves[current_move])
            render_svg(chess.svg.board(board))
            st.write(f'current_move is {current_move}')
        else: 
            st.write('error you idiot')
            st.write(f'current_move is {current_move}')


# moves = [move for move in m_defense.mainline_moves()]



    # chess.Move.from_uci(user_move) in board.legal_moves and
        

#Documentation for this specific function (game move slidebar)


# st.write(moves[2])

# mv = st.slider("Move",0,len(moves),len(moves))

# for move in moves[0:mv]:
#     board.push(move)

# def render_svg(svg):
#     """Renders the given svg string."""
#     b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
#     html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
#     st.write(html, unsafe_allow_html=True)

# render_svg(chess.svg.board(board))
