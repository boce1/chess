import pygame
from constants import WIDTH, HEIGHT, WHITE, BLACK, FPS
from board_util import *

pygame.init()

class Main_window:
    def __init__(self):  
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')

        self.board = Board()

    def draw(self):
        self.window.fill(WHITE)
        self.board.draw(self.window)
        pygame.display.update()

    def display(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                self.board.move_piece(mouse_pos, event)
                self.board.choose_promoting_piece(mouse_pos, event)

            self.draw()
        
        pygame.quit()