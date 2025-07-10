from .pawn_logic import get_available_moves_pawn
from .rook_logic import get_available_moves_rook
from .bishop_logic import get_available_moves_bishop
from .queen_logic import get_available_moves_queen
from .knight_logic import get_available_moves_knight
from .king_logic import get_available_moves_king

def get_available_moves(board_state, piece_pos):
    piece = board_state[piece_pos[0]][piece_pos[1]]
    out = []
    if piece:
        if piece[1] == 'p':
            out = get_available_moves_pawn(board_state, piece_pos)
        if piece[1] == 'r':
            out = get_available_moves_rook(board_state, piece_pos)
        if piece[1] == 'b':
            out = get_available_moves_bishop(board_state, piece_pos)
        if piece[1] == 'q':
            out = get_available_moves_queen(board_state, piece_pos)
        if piece[1] == 'k':
            out = get_available_moves_knight(board_state, piece_pos)
        if piece[1] == 'K':
            out = get_available_moves_king(board_state, piece_pos)

    return out 
           