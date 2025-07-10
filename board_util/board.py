'''
8x8 grid
format string piece: [color][piece]
color - w/b
piece - p/r/k/b/q/K
column - a/b/c/d/e/f/g/h
row - 1/2/3/4/5/6/7/8
'''
from constants import CELL_WIDHT, BLACK_CELLS_COLOR, WHITE_CELLS_COLOR, WIDTH, HEIGHT, BLACK, WHITE, AVAILABLE_CELLS_COLOR, FRAME_PADDING
import pygame
from .piece_logic import *
from .pawn_logic import *
import os

class Board:
    def __init__(self):
        self.start_x = WIDTH // 2 - 4 * CELL_WIDHT
        self.start_y = HEIGHT // 2 - 4 * CELL_WIDHT

        self.initialize()

        base_path = os.path.dirname(os.path.abspath(__file__))
        pics_path = os.path.join(base_path, 'pics')

        self.white_king = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'white', 'king.png')), (CELL_WIDHT, CELL_WIDHT))
        self.black_king = pygame.transform.scale(pygame.image.load((os.path.join(pics_path, 'black', 'king.png'))), (CELL_WIDHT, CELL_WIDHT))

        self.white_queen = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'white', 'queen.png')), (CELL_WIDHT, CELL_WIDHT))
        self.black_queen = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'black', 'queen.png')), (CELL_WIDHT, CELL_WIDHT))

        self.white_knight = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'white', 'knight.png')), (CELL_WIDHT, CELL_WIDHT))
        self.black_knight = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'black', 'knight.png')), (CELL_WIDHT, CELL_WIDHT))

        self.white_bishop = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'white', 'bishop.png')), (CELL_WIDHT, CELL_WIDHT))
        self.black_bishop = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'black', 'bishop.png')), (CELL_WIDHT, CELL_WIDHT))

        self.white_rook = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'white', 'rook.png')), (CELL_WIDHT, CELL_WIDHT))
        self.black_rook = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'black', 'rook.png')), (CELL_WIDHT, CELL_WIDHT))

        self.white_pawn = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'white', 'pawn.png')), (CELL_WIDHT, CELL_WIDHT))
        self.black_pawn = pygame.transform.scale(pygame.image.load(os.path.join(pics_path, 'black', 'pawn.png')), (CELL_WIDHT, CELL_WIDHT))

        self.moving_cords = None

        self.turn = False # False white's turn, True black's turn
        self.promoting = 0 # 0 for no promoting a pawn, 1 for white promoting, 2 for black promoting
        self.promoting_cords = None

        self.y_promoting_rect = [self.start_y + 2*CELL_WIDHT + i*CELL_WIDHT for i in range(4)]
        self.x_promoting_rect_white = self.start_x + 8*CELL_WIDHT
        self.x_promoting_rect_black = x = self.start_x - CELL_WIDHT

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

        # pawn testing
        # self.state = [
        #     [None for _ in range(8)],
        #     ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
        #     [None for _ in range(8)],
        #     [None for _ in range(8)],
        #     [None for _ in range(8)],
        #     [None for _ in range(8)],
        #     ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
        #     [None for _ in range(8)],
        # ]

        # rook testing
        self.state = [
            ['br', 'br', 'br', 'bK', 'br','br', 'br', 'br'],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            ['wr', 'wr', 'wr', 'wK', 'wr','wr', 'wr', 'wr'],
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
                    pygame.draw.rect(win, AVAILABLE_CELLS_COLOR, (self.start_x+self.moving_cords[1]*CELL_WIDHT, self.start_y+self.moving_cords[0]*CELL_WIDHT, CELL_WIDHT, CELL_WIDHT))
                    for cords in get_available_moves(self.state, self.moving_cords):
                        pygame.draw.rect(win, AVAILABLE_CELLS_COLOR, (self.start_x + cords[1]*CELL_WIDHT, 
                                                                      self.start_y+ cords[0]*CELL_WIDHT,
                                                                    CELL_WIDHT, CELL_WIDHT), 3)
                        

        pygame.draw.rect(win, BLACK, (self.start_x-FRAME_PADDING, self.start_y-FRAME_PADDING, 
                                      8*CELL_WIDHT+2*FRAME_PADDING, 8*CELL_WIDHT+2*FRAME_PADDING), 3)

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

    def promoting_choice_rect(self, win):
        if self.promoting == 1:
            pygame.draw.rect(win, BLACK, (self.x_promoting_rect_white, self.y_promoting_rect[0], CELL_WIDHT, 4*CELL_WIDHT))
            win.blit(self.white_queen, (self.x_promoting_rect_white, self.y_promoting_rect[0]))
            win.blit(self.white_rook, (self.x_promoting_rect_white, self.y_promoting_rect[1]))
            win.blit(self.white_knight, (self.x_promoting_rect_white, self.y_promoting_rect[2]))
            win.blit(self.white_bishop, (self.x_promoting_rect_white, self.y_promoting_rect[3]))
        elif self.promoting == 2:
            pygame.draw.rect(win, WHITE, (self.x_promoting_rect_black, self.y_promoting_rect[0], CELL_WIDHT, 4*CELL_WIDHT))
            pygame.draw.rect(win, BLACK, (self.x_promoting_rect_black, self.y_promoting_rect[0], CELL_WIDHT, 4*CELL_WIDHT), 2)
            win.blit(self.black_queen, (self.x_promoting_rect_black, self.y_promoting_rect[0]))
            win.blit(self.black_rook, (self.x_promoting_rect_black, self.y_promoting_rect[1]))
            win.blit(self.black_knight, (self.x_promoting_rect_black, self.y_promoting_rect[2]))
            win.blit(self.black_bishop, (self.x_promoting_rect_black, self.y_promoting_rect[3]))

    def choose_promoting_piece(self, mouse_pos, event):
        x = mouse_pos[0]
        y = mouse_pos[1]

        index = None
        if ( (self.x_promoting_rect_white <= x <= self.x_promoting_rect_white + CELL_WIDHT or 
                self.x_promoting_rect_black <= x <= self.x_promoting_rect_black + CELL_WIDHT) and
                    self.y_promoting_rect[0] <= y <= self.y_promoting_rect[len(self.y_promoting_rect)-1]+CELL_WIDHT and
                        event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                index = (y - self.y_promoting_rect[0]) // CELL_WIDHT
        
        if index != None:
            promoting_pieces = get_promotable_pieces(self.state, self.promoting_cords)
            if promoting_pieces:
                promoting_piece = promoting_pieces[index]
                self.state[self.promoting_cords[0]][self.promoting_cords[1]] = promoting_piece
            self.promoting_cords = None
            self.promoting = 0

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
                        (self.state[row][col][0] == 'b' and not self.turn) or 
                        self.promoting != 0): # black's turn but white selected
                        self.moving_cords = None
                else:
                    if (row, col) in get_available_moves(self.state, self.moving_cords):
                        self.state[row][col] = self.state[self.moving_cords[0]][self.moving_cords[1]]
                        self.state[self.moving_cords[0]][self.moving_cords[1]] = None
                        
                        en_passant(self.state, (row, col)) # check for en passant
                        self.turn = not self.turn

                        self.promoting = can_be_promoted(self.state, (row, col))
                        if self.promoting != 0:
                            self.promoting_cords = (row, col)

                    self.moving_cords = None

    def draw(self, win):
        self.draw_frame(win)
        self.draw_pieces(win)
        self.promoting_choice_rect(win)

        