import base64
import streamlit as st
import chess, chess.pgn



class Classboard: 
    
    def __init__(self, variation):
        #board = m_defense.board()
        self.variation = variation
        ##This may not work
        self.variation_board = variation.board()
        self.move_count = 0
    
    def render_svg(self, svg):
        """Renders the given svg string."""
        b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
        st.write(html, unsafe_allow_html=True)
        
    def display_render(self):
        """visualize chess board"""
        self.render_svg(chess.svg.board(self.variation_board))
        
    def reset_move_count(self):
        """assigns zero to move_count"""
        self.move_count = 0
        
    def plus_one_move_count(self):
        """increases move_count by one"""
        self.move_count += 1
        
    def generate_correct_move_list(self):
        """generates list of correct moves to check against user submitted moves"""
        self.move_list = [move for move in self.variation.mainline_moves()]
    
    def make_correct_move_on_board(self): 
        """Correctly moves the chess pieces according to the given pgn"""   
        self.variation_board.push(self.move_list[self.move_count])
        
    def return_correct_move_string(self):
        "return stringifed version of correct move"
        return str(self.move_list[self.move_count])

