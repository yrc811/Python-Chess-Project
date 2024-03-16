import pygame
import time
from chess.constants import width, height, dark_pink, light_pink, rows, columns, square_size
from chess.board import Board
from chess.pieces import piece
from chess.game import Game
pygame.init()
FPS = 60



'''
startingPosition = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
def fenToBoard(fen):'''
def get_row_col(pos):
    
    x,y = pos
    return (x//square_size, y//square_size)




screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

running = True
game = Game(screen)
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x,y = get_row_col(pos)
            
            game.select(y,x)
            
            
          
    game.update()
    clock.tick(FPS)
    
pygame.quit()