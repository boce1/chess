from .rook_logic import get_available_moves_rook
from .bishop_logic import get_available_moves_bishop

def get_available_moves_queen(board_state, piece_pos):
    out = get_available_moves_rook(board_state, piece_pos) # same as rook + diagonals
    out.extend(get_available_moves_bishop(board_state, piece_pos))
    return out
