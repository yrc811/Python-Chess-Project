import pygame

class piece:
    def __init__(self,type,row,col,colour):
        self.row = row
        self.column = col
        self.colour = colour
        self.type = type
        self.icon = pygame.image.load("chess/Assets/"+str(colour+type)+".png")
        self.has_castled = True
        if type == "k" or type == "r":
            self.has_castled = False
    
    def display_piece(self,screen):
        screen.blit(self.icon,((self.column)*125,(self.row)*125))
        
    def change_pos (self,row,column):
        self.row = row
        self.column = column
        