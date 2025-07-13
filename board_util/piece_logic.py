from .pawn_logic import get_available_moves_pawn, get_pawn_taking_moves, change_state_of_moved_pawns, get_pawn_taking_moves_in_every_case, change_permission_for_en_passant
from .rook_logic import get_available_moves_rook
from .bishop_logic import get_available_moves_bishop
from .queen_logic import get_available_moves_queen
from .knight_logic import get_available_moves_knight
from .king_logic import get_available_moves_king, get_available_moves_castle, change_state_of_moved_kings_rooks, king_castle
from .king_pos import find_king_pos
import copy

def get_opp_moves(board_state, piece_pos): # piece pos is king
    out = []
    temp_king = board_state[piece_pos[0]][piece_pos[1]]
    board_state[piece_pos[0]][piece_pos[1]] = None
    for i in range(8):
        for j in range(8):
            if (board_state[i][j] and 
                board_state[i][j][0] != temp_king[0]):
                opp_piece = board_state[i][j][1]
                pos = (i, j)
                if opp_piece == 'p':
                    moves = get_pawn_taking_moves(board_state, pos)
                elif opp_piece == 'q':
                    moves = get_available_moves_queen(board_state, pos)
                elif opp_piece == 'r':
                    moves = get_available_moves_rook(board_state, pos)
                elif opp_piece == 'b':
                    moves = get_available_moves_bishop(board_state, pos)
                elif opp_piece == 'k':
                    moves = get_available_moves_knight(board_state, pos)
                else:
                    moves = []
                out.extend(set(moves))
                out.extend(get_pawn_taking_moves_in_every_case(board_state, temp_king[0]))
    board_state[piece_pos[0]][piece_pos[1]] = temp_king
    return out

def is_check(board_state, piece_pos): # piece pos is king
    row = piece_pos[0]
    col = piece_pos[1]
    if board_state[row][col][1] == 'K':
        if piece_pos in get_opp_moves(board_state, piece_pos):
            return True
        return False
    else:
        raise "The piece is not king!"


def get_available_moves(board_state, piece_pos, are_pawns_moved, are_kings_rook_moved, permission_for_en_passant):
    row = piece_pos[0]
    col = piece_pos[1]
    piece = board_state[row][col]
    color = piece[0]
    out = []
    if piece:
        if piece[1] == 'p':
            out = get_available_moves_pawn(board_state, piece_pos, are_pawns_moved, permission_for_en_passant)
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
            out = [x for x in out if not (x in get_opp_moves(board_state, piece_pos))]
            out = [x for x in out if not (x in get_pawn_taking_moves_in_every_case(board_state, color))]

            if not is_check(board_state, piece_pos): # castle if not chekc
                castle_pos = get_available_moves_castle(board_state, piece_pos, out, are_kings_rook_moved)

                out_remove = set()
                for pair in castle_pos: # ckeck if is check in cell that is further away from king
                    temp_board = copy.deepcopy(board_state)
                    temp_piece = temp_board[row][col]
                    temp_board[row][col] = None
                    temp_board[pair[0]][pair[1]] = temp_piece

                    if is_check(temp_board, pair):
                        out_remove.add(pair)
                
                castle_pos = [x for x in castle_pos if not (x in out_remove)]
                out.extend(castle_pos)

        if piece[1] != 'K': # filter moves that make king in check possition
            king_pos = find_king_pos(board_state, color)
            out_filtered = []
            for pair in out:
                temp_board = copy.deepcopy(board_state)
                temp_piece = temp_board[row][col]
                temp_board[row][col] = None
                temp_board[pair[0]][pair[1]] = temp_piece

                if not is_check(temp_board, king_pos):
                    out_filtered.append(pair)
                del temp_board
            return out_filtered
        else: # filter moves that king takes defended pieces
            out_filtered = []
            for pair in out:
                temp_board = copy.deepcopy(board_state)
                temp_piece = temp_board[row][col]
                temp_board[row][col] = None
                temp_board[pair[0]][pair[1]] = temp_piece

                if not is_check(temp_board, pair):
                    out_filtered.append(pair)
                del temp_board
            return out_filtered

    return out 

def is_white_in_checkmate(board_state):
    white_king_pos = find_king_pos(board_state, 'w')
    # No need for:  are_pawns_moved, are_kings_rook_moved, permission_for_en_passant
    if (is_check(board_state, white_king_pos) and
        len(get_available_moves(board_state, white_king_pos, None, None, None)) == 0):
        return True
    return False

def is_black_in_checkmate(board_state):
    black_king_pos = find_king_pos(board_state, 'b')
    # No need for:  are_pawns_moved, are_kings_rook_moved, permission_for_en_passant
    if (is_check(board_state, black_king_pos) and 
        len(get_available_moves(board_state, black_king_pos, None, None, None)) == 0):
        return True
    return False

def is_white_in_stalemate(board_state, are_pawns_moved, are_kings_rook_moved, permission_for_en_passant):
    white_king_pos = find_king_pos(board_state, 'w')
    available_moves = 0
    for i in range(8):
        for j in range(8):
            piece = board_state[i][j]
            if piece and piece[0] == 'w':
                available_moves += len(get_available_moves(board_state, (i, j), are_pawns_moved, are_kings_rook_moved, permission_for_en_passant))

    if (not is_check(board_state, white_king_pos) and
        available_moves == 0):
        return True
    return False

def is_black_in_stalemate(board_state, are_pawns_moved, are_kings_rook_moved, permission_for_en_passant):
    black_king_pos = find_king_pos(board_state, 'b')
    available_moves = 0
    for i in range(8):
        for j in range(8):
            piece = board_state[i][j]
            if piece and piece[0] == 'b':
                available_moves += len(get_available_moves(board_state, (i, j), are_pawns_moved, are_kings_rook_moved, permission_for_en_passant))

    if (not is_check(board_state, black_king_pos) and
        available_moves == 0):
        return True
    return False

def is_draw(board_state):
    white_pieces = []
    black_pieces = []

    for i in range(8):
        for j in range(8):
            piece = board_state[i][j]
            if piece:
                if piece[0] == 'w':
                    white_pieces.append(piece)
                elif piece[0] == 'b':
                    black_pieces.append(piece)

    if len(white_pieces) == len(black_pieces) and white_pieces[0] == 'wK' and black_pieces[0] == 'bK':
        return True
    
    if len(white_pieces) == 2 and len(black_pieces) == 1:
        if 'wK' in white_pieces and 'wb' in white_pieces and 'bK' in black_pieces:
            return True
        if 'wK' in white_pieces and 'wk' in white_pieces and 'bK' in black_pieces:
            return True
        
    if len(black_pieces) == 2 and len(white_pieces) == 1:
        if 'bK' in black_pieces and 'bb' in black_pieces and 'wK' in white_pieces:
            return True
        if 'bK' in black_pieces and 'bk' in black_pieces and 'wK' in white_pieces:
            return True
        
    if len(black_pieces) == 2 and len(white_pieces) == 2:
        if 'bK' in black_pieces and 'bb' in black_pieces and 'wK' in white_pieces and 'wb' in white_pieces:
            bishops_pos = []
            for i in range(8): # find bishops
                for j in range(8):
                    if board_state[i][j] and board_state[i][j][1] == 'b':
                        bishops_pos.append((i, j))
            if sum(bishops_pos[0]) % 2 == sum(bishops_pos[1]) % 2:
                return True
    return False