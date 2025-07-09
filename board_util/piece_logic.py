from .pawn_logic import get_available_moves_pawn

def get_available_moves(board_state, piece_pos):
    piece = board_state[piece_pos[0]][piece_pos[1]]
    out = []
    if piece:
        if piece[1] == 'p':
            out = get_available_moves_pawn(board_state, piece_pos, piece[0])
    return out            