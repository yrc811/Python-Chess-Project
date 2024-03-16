import pygame
from chess.board import Board
from chess.constants import grey, square_size

class Game:
    def __init__(self,win):
        self._init()
        self.win = win
    def _init(self):
        self.selected_piece = None
        self.board = Board()
        self.turn = "w"
        self.valid_moves = []
            
    def update(self):
        self.board.draw_pieces(self.win)
        if len(self.valid_moves) > 0:
            if self.selected_piece:
                self.show_valid_moves(self.win)
        pygame.display.flip()
        
    
    def reset(self):
        self._init()
        
    def select(self,row,column):
        if self.selected_piece:
            result_from_move = self._move(row,column)
            if not result_from_move:
                self.selected_piece = None
                self.select(row,column)
        else:
            piece = self.board.get_piece(row,column)
            if piece != "" and piece.colour == self.turn:
                self.selected_piece = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                #print(self.board.get_movable_squares(self.turn))
                return True
            return False
        
    def show_valid_moves(self,win):
        for item in self.valid_moves:
            row,column = item[0],item[1]
            circle_x, circle_y = column*square_size, row*square_size
            circle_x, circle_y = circle_x+(square_size//2),circle_y+(square_size//2)
            pygame.draw.circle(win,grey,[circle_x,circle_y],20)
            
    def _move(self,row,column):
        
        if self.selected_piece and (row,column) in self.valid_moves:
            #print("N1")
            if self.board.king_safety_check(self.selected_piece,row,column) == True:
                self.board.move_piece(self.selected_piece,row,column)
                self.change_turn()
                self.selected_piece = None
                self.valid_moves = []
            elif self.board.king_safety_check == False:
                #print("N2")
                return False
        else:
            return False
        return True
    
    def change_turn(self):
        if self.turn == "w":
            self.turn = "b"
        else:
            self.turn = "w"