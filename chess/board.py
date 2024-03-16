import pygame 
from chess.constants import height, width, dark_pink, light_pink, square_size, rows, columns
from chess.pieces import piece

class Board:
    def __init__(self):
        self.board = [["br","bn","bb","bq","bk","bb","bn","br"],
                      ["bp","bp","bp","bp","bp","bp","bp","bp"],
                      [""]*8,[""]*8,[""]*8,[""]*8,
                      ["wp","wp","wp","wp","wp","wp","wp","wp"],
                      ["wr","wn","wb","wq","wk","wb","wn","wr"],]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != "":
                    self.board[i][j] = piece(self.board[i][j][1],i,j,self.board[i][j][0])
        
        
    def draw_squares(self,screen):
        screen.fill(dark_pink)
        for row in range(rows):
            for column in range(row%2,columns,2):
                pygame.draw.rect(screen,light_pink,[column*square_size,row*square_size,square_size,square_size])
           
    def draw_pieces(self,screen):
        self.draw_squares(screen)
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != "":
                    self.board[i][j].display_piece(screen)
    def get_piece(self,row,column):
        return self.board[row][column]                
    
    def move_piece(self,piece,row,column):
        
        self.board[piece.row][piece.column],self.board[row][column] = "",self.board[piece.row][piece.column]
        piece.change_pos(row,column)
        
    def is_occupied(self,row,column):
        if self.board[row][column] == "":
            return False
        return True
    
    def is_same_colour(self,piece,row,column):
        if self.is_occupied(row,column):
            piece_colour = piece.colour
            piece_to_move = self.get_piece(row,column)
            piece_to_move_colour = piece_to_move.colour
            if piece_to_move_colour == piece_colour:
                return True
        return False
    
    def pawn_capture_check(self,piece):
        valid_moves = []
        if piece.colour == "b":
            direction = 1
        else:
            direction = -1
        if piece.column > 0:
            if self.is_occupied(piece.row+direction ,piece.column-1) and not(self.is_same_colour(piece,piece.row + direction,piece.column-1)):
                valid_moves.append((piece.row+direction ,piece.column-1))     
        if piece.column < 7:
            if self.is_occupied(piece.row+direction ,piece.column+1) and not(self.is_same_colour(piece,piece.row + direction,piece.column+1)):
                valid_moves.append((piece.row+direction ,piece.column+1))
        return valid_moves
    
    def diagonal_scan(self,piece):
        valid_moves = []
        row,column = piece.row,piece.column
        modifiers = [(-1,-1),(-1,1),(1,-1),(1,1)]
        for item in modifiers:
            modifier_1 = item[0]
            modifier_2 = item[1]
            for i in range(1,8):
                x_distance = modifier_1*i
                y_distance = modifier_2*i
                if 0 <= row+y_distance <= 7 and 0 <= column + x_distance <= 7:
                    if self.is_occupied(row+y_distance,column+x_distance):
                        if self.is_same_colour(piece,row+y_distance,column+x_distance):
                            break
                        elif not(self.is_same_colour(piece,row+y_distance,column+x_distance)):
                            valid_moves.append((row+y_distance,column+x_distance))
                            break
                    elif not(self.is_occupied(row+y_distance,column+x_distance)):
                        valid_moves.append((row+y_distance,column+x_distance))
                else:
                    break
        return valid_moves           
    def parallel_scan(self,piece):
        valid_moves = []
        row,column = piece.row,piece.column
        multiplier = [(1,0),(-1,0),(0,1),(0,-1)]
        for item in multiplier:
            column_distance = item[0]
            row_distance = item[1]
            for i in range(1,8):
                new_row = row + (i*row_distance)
                new_column = column + (i*column_distance)
                
                if (0<= new_row <= 7) and (0<= new_column <= 7):
    
                    if self.is_occupied(new_row,new_column):
                        if self.is_same_colour(piece,new_row,new_column):
                            break
                        elif not(self.is_same_colour(piece,new_row,new_column)):
                            valid_moves.append((new_row , new_column))
                            break
                    else:
                        valid_moves.append((new_row , new_column))
        
        return valid_moves
    def get_movable_squares(self,colour):
        possible_squares = set()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != "":
                    if self.board[i][j].colour != colour and self.board[i][j].type != "k":
                        for item in self.get_valid_moves(self.board[i][j]):
                            possible_squares.add(item)
        return list(possible_squares)        
    
    def king_safety_check(self,piece,row,column):
        board_copy = Board()
        for board_row in range(8):
            for board_column in range(8):
                board_copy.board[board_row][board_column] = self.board[board_row][board_column]
                if board_copy.board[board_row][board_column] != "":
                    if board_copy.board[board_row][board_column].type == "k" and board_copy.board[board_row][board_column].colour == piece.colour:
                        king_pos = (board_row,board_column)
        board_copy.board[row][column], board_copy.board[piece.row][piece.column] = board_copy.board[piece.row][piece.column], ""
        dangers = board_copy.get_movable_squares(piece.colour)
        if king_pos in dangers:
            return False
        return True 
                        
    def get_valid_moves(self,piece):
        valid_moves = []
        if piece.type == "p":
            if piece.colour == "w" and piece.row == 6:
                for i in range(1,3):
                    if not(self.is_occupied(piece.row-i,piece.column)):
                        valid_moves.append((piece.row-i,piece.column))
                    elif self.is_occupied(piece.row-i,piece.column):
                        break  
            elif piece.colour == "b" and piece.row == 1:
                for i in range(1,3):
                    if not(self.is_occupied(piece.row+i,piece.column)):
                        valid_moves.append((piece.row+i,piece.column))
                    elif self.is_occupied(piece.row+i,piece.column):
                        break
                    
            elif piece.colour == "w":
                if not(self.is_occupied(piece.row-1,piece.column)):
                    valid_moves.append((piece.row-1,piece.column))
            elif piece.colour == "b":
                if not(self.is_occupied(piece.row+1,piece.column)):
                    valid_moves.append((piece.row+1,piece.column))
            valid_moves = valid_moves + self.pawn_capture_check(piece)
            
        if piece.type == "n":
            x,y = piece.column, piece.row
            x_moves = [2,-2]
            y_moves = [1,-1]
            for x_move in x_moves:
                for y_move in y_moves:
                    if 0 <= x + x_move <= 7 and 0 <= y + y_move <= 7:
                        valid_moves.append((y+y_move,x+x_move))
                    if 0<= x + y_move <= 7 and 0 <= y + x_move<= 7:
                        valid_moves.append((y+x_move,x+y_move))    
            valid_moves_copy = valid_moves.copy()      
            valid_moves = []    
            for item in valid_moves_copy:
                row,column = item[0],item[1]
                if not(self.is_same_colour(piece,row,column)):
                    valid_moves.append(item)
                    
        if piece.type == "b":
            valid_moves = self.diagonal_scan(piece)
        
        if piece.type == "r":
            valid_moves = self.parallel_scan(piece)        
        if piece.type == "q":
            valid_moves = self.parallel_scan(piece) + self.diagonal_scan(piece)        
            
        if piece.type == "k":
             
            x_moves = [-1,0,1]    
            y_moves = [-1,0,1]
            non_check_squares = self.get_movable_squares(piece.colour)
            for i in range(3):
                for j in range(3):
                    if 0 <= piece.row + y_moves[i] <= 7 and 0 <= piece.column + x_moves[j] <= 7:
                        if (piece.row+y_moves[i],piece.column+x_moves[j]) not in non_check_squares:
                            if not(self.is_same_colour(piece,piece.row+y_moves[i],piece.column+x_moves[j])):
                                valid_moves.append((piece.row+y_moves[i],piece.column+x_moves[j]))
                        
                 
        return valid_moves
                    
                        
            
    