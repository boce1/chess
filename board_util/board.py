'''
8x8 grid
format string piece: [color][piece]
color - w/b
piece - p/r/k/b/q/K
column - a/b/c/d/e/f/g/h
row - 1/2/3/4/5/6/7/8
'''
from constants import CELL_WIDHT, BLACK_CELLS_COLOR, WHITE_CELLS_COLOR, WIDTH, HEIGHT, BLACK, AVAILABLE_CELLS_COLOR
import pygame
from .piece_logic import *
from .pawn_logic import en_passant

class Board:
    def __init__(self):
        self.start_x = WIDTH // 2 - 4 * CELL_WIDHT
        self.start_y = HEIGHT // 2 - 4 * CELL_WIDHT

        self.initialize()

        self.white_king = pygame.transform.scale(pygame.image.load(r'./board_util/pics/white/king.png'), (CELL_WIDHT, CELL_WIDHT))
        self.black_king = pygame.transform.scale(pygame.image.load(r'./board_util/pics/black/king.png'), (CELL_WIDHT, CELL_WIDHT))

        self.white_queen = pygame.transform.scale(pygame.image.load(r'./board_util/pics/white/queen.png'), (CELL_WIDHT, CELL_WIDHT))
        self.black_queen = pygame.transform.scale(pygame.image.load(r'./board_util/pics/black/queen.png'), (CELL_WIDHT, CELL_WIDHT))

        self.white_knight = pygame.transform.scale(pygame.image.load(r'./board_util/pics/white/knight.png'), (CELL_WIDHT, CELL_WIDHT))
        self.black_knight = pygame.transform.scale(pygame.image.load(r'./board_util/pics/black/knight.png'), (CELL_WIDHT, CELL_WIDHT))

        self.white_bishop = pygame.transform.scale(pygame.image.load(r'./board_util/pics/white/bishop.png'), (CELL_WIDHT, CELL_WIDHT))
        self.black_bishop = pygame.transform.scale(pygame.image.load(r'./board_util/pics/black/bishop.png'), (CELL_WIDHT, CELL_WIDHT))

        self.white_rook = pygame.transform.scale(pygame.image.load(r'./board_util/pics/white/rook.png'), (CELL_WIDHT, CELL_WIDHT))
        self.black_rook = pygame.transform.scale(pygame.image.load(r'./board_util/pics/black/rook.png'), (CELL_WIDHT, CELL_WIDHT))

        self.white_pawn = pygame.transform.scale(pygame.image.load(r'./board_util/pics/white/pawn.png'), (CELL_WIDHT, CELL_WIDHT))
        self.black_pawn = pygame.transform.scale(pygame.image.load(r'./board_util/pics/black/pawn.png'), (CELL_WIDHT, CELL_WIDHT))

        self.moving_cords = None

        self.turn = False # False white's turn, True black's turn

    def initialize(self):
        self.state = [
            ['br', 'bk', 'bb', 'bq', 'bK','bb', 'bk', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wk', 'wb', 'wq', 'wK','wb', 'wk', 'wr']
        ]


    def draw_frame(self, win):
        for i in range(8):
            for j in range(8):
                
                if (i + j) % 2 == 1:
                    color_cell = BLACK_CELLS_COLOR
                else:
                    color_cell = WHITE_CELLS_COLOR

                pygame.draw.rect(win, color_cell, (self.start_x + i*CELL_WIDHT, self.start_y+ j*CELL_WIDHT,
                                    CELL_WIDHT, CELL_WIDHT))
                
                if self.moving_cords and self.state[self.moving_cords[0]][self.moving_cords[1]]:
                    for cords in get_available_moves(self.state, self.moving_cords):
                        pygame.draw.rect(win, AVAILABLE_CELLS_COLOR, (self.start_x + cords[1]*CELL_WIDHT, 
                                                                      self.start_y+ cords[0]*CELL_WIDHT,
                                                                    CELL_WIDHT, CELL_WIDHT), 3)
                        

        pygame.draw.rect(win, BLACK, (self.start_x, self.start_y, 8*CELL_WIDHT, 8*CELL_WIDHT), 3)

    def draw_pieces(self, win):
        for row in range(8):
            for col in range(8):
                piece = self.state[row][col]
                if piece:
                    if piece[0] == 'w':
                        if piece[1] == 'p':
                            win.blit(self.white_pawn, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                        elif piece[1] == 'r':
                            win.blit(self.white_rook, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                        elif piece[1] == 'k':
                            win.blit(self.white_knight, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                        elif piece[1] == 'q':
                            win.blit(self.white_queen, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                        elif piece[1] == 'b':
                            win.blit(self.white_bishop, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                        elif piece[1] == 'K':
                            win.blit(self.white_king, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                    else:
                        if piece[1] == 'p':
                            win.blit(self.black_pawn, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                        elif piece[1] == 'r':
                            win.blit(self.black_rook, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                        elif piece[1] == 'k':
                            win.blit(self.black_knight, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                        elif piece[1] == 'q':
                            win.blit(self.black_queen, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                        elif piece[1] == 'b':
                            win.blit(self.black_bishop, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))
                        elif piece[1] == 'K':
                            win.blit(self.black_king, (self.start_x + col*CELL_WIDHT, self.start_y + row*CELL_WIDHT))

    def move_piece(self, mouse_pos, event):
        x = mouse_pos[0]
        y = mouse_pos[1]
        if (self.start_x <= x <= self.start_x + 8*CELL_WIDHT and
            self.start_y <= y <= self.start_y + 8*CELL_WIDHT): # is mouse on the board

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                row = (y - self.start_y) // CELL_WIDHT
                col = (x - self.start_x) // CELL_WIDHT

                if not self.moving_cords:
                    self.moving_cords = (row, col)
                    if (not self.state[self.moving_cords[0]][self.moving_cords[1]] or # if no piece is selected
                        (self.state[row][col][0] == 'w' and self.turn) or # if white's turn but black selected
                        (self.state[row][col][0] == 'b' and not self.turn)): # black's turn but white selected
                        self.moving_cords = None
                    #print(get_available_moves(self.state, self.moving_cords) )
                else:
                    if (row, col) in get_available_moves(self.state, self.moving_cords):
                        self.state[row][col] = self.state[self.moving_cords[0]][self.moving_cords[1]]
                        self.state[self.moving_cords[0]][self.moving_cords[1]] = None
                        
                        en_passant(self.state, (row, col)) # check for en passant
                        self.turn = not self.turn

                    self.moving_cords = None

    def draw(self, win):
        self.draw_frame(win)
        self.draw_pieces(win)

        