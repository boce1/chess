from .rook_logic import get_available_moves_rook
from .bishop_logic import get_available_moves_bishop

def get_available_moves_queen(board_state, piece_pos):
    color = board_state[piece_pos[0]][piece_pos[1]][0]
    out = get_available_moves_rook(board_state, piece_pos) # same as rook + diagonals
    out.extend(get_available_moves_bishop(board_state, piece_pos))
    

    return out
