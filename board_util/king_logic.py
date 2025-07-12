from .pawn_logic import get_available_moves_pawn
from .knight_logic import get_available_moves_knight
from .queen_logic import get_available_moves_queen
from .bishop_logic import get_available_moves_bishop
from .rook_logic import get_available_moves_rook
from .king_pos import find_king_pos

def get_available_moves_king(board_state, piece_pos):
    out = []
    row = piece_pos[0]
    col = piece_pos[1]
    color = board_state[row][col][0]

    for i in range(2): # bellow and upper row
        for j in range(3):
            out.append((row + (-1)**i, col+(j-1)))
    out.append((row, col-1))
    out.append((row, col+1))

    oposite_king_pos = None
    if color == 'w':
        opp_color = 'b'
    else:
        opp_color = 'w'
    oposite_king_pos = find_king_pos(board_state, opp_color)

    remove_list = set()
    for pair in out:
        flag_removed = False
        if pair[0] < 0 or pair[0] > 7:
            remove_list.add(pair)
            flag_removed = True
        if pair[1] < 0 or pair[1] > 7:
            remove_list.add(pair)
            flag_removed = True

        if not flag_removed:
            if board_state[pair[0]][pair[1]] and board_state[pair[0]][pair[1]][1] == 'K':
                remove_list.add(pair)
            if board_state[pair[0]][pair[1]] and board_state[pair[0]][pair[1]][0] == color:
                remove_list.add(pair)

            # oposite king possition
            row_diff = abs(pair[0] - oposite_king_pos[0])
            col_diff = abs(pair[1] - oposite_king_pos[1])

            if row_diff == 1 and col_diff == 0:
                remove_list.add(pair)

            elif col_diff == 1 and row_diff == 0:
                remove_list.add(pair)

            elif col_diff == 1 and row_diff == 1:
                remove_list.add(pair)

    out = [x for x in out if not (x in remove_list)]
    return out

def find_rooks(board_state):
    out = []
    for i in range(8):
        for j in range(8):
            if board_state[i][j][1] == 'r':
                out.append((board_state[i][j][0], (i, j)))
    return out

def get_available_moves_castle(board_state, piece_pos, available_moves, are_kings_rook_moved):
    '''
    are_kings_rook_moved
    # first 3 white - rook, king, rook
    # second 3 black - rook, king, rook
    '''
    out = []
    row = piece_pos[0]
    col = piece_pos[1]
    color = board_state[row][col][0]
    piece = board_state[row][col][1]

    if piece == 'K':
        # white 
        if color == 'w' and row == 7 and col == 4: # is king on the right cell
            if not (are_kings_rook_moved[0] or are_kings_rook_moved[1]): # are left rook and king moved
            # left rook
                if board_state[7][0] and board_state[7][0][1] == 'r':  # is left rook on the right cell
                    if ((7,3) in available_moves and 
                        board_state[7][1] == None and board_state[7][2] == None): # if king is not passing cells where ckeck and cells righ to rook are free
                        out.append((7, 2))

                # right rook
            if not (are_kings_rook_moved[1] or are_kings_rook_moved[2]): # are king and right rook moved
                if board_state[7][7] and board_state[7][7][1] == 'r':
                    if ((7, 5) in available_moves and 
                        board_state[7][5] == None and board_state[7][6] == None):
                        out.append((7, 6))

        # black
        elif color == 'b' and row == 0 and col == 4: # is king on the right cell
            if not (are_kings_rook_moved[3] or are_kings_rook_moved[4]): # are left rook and king moved
            # left rook
                if board_state[0][0] and board_state[0][0][1] == 'r':  # is left rook on the right cell
                    if ((0,3) in available_moves and 
                        board_state[0][1] == None and board_state[0][2] == None): # if king is not passing cells where ckeck and cells righ to rook are free
                        out.append((0, 2))

            if not (are_kings_rook_moved[4] or are_kings_rook_moved[5]): # are right rook and king moved
                # right rook
                if board_state[0][7] and board_state[0][7][1] == 'r':  # is left rook on the right cell
                    if ((0,5) in available_moves and 
                        board_state[0][5] == None and board_state[0][6] == None): # if king is not passing cells where ckeck and cells righ to rook are free
                        out.append((0, 6))
    return out

def change_state_of_moved_kings_rooks(board_state, are_kings_rook_moved):
    if board_state[7][0] != 'wr':
        are_kings_rook_moved[0] = True
    if board_state[7][4] != 'wK':
        are_kings_rook_moved[1] = True
    if board_state[7][7] != 'wr':
        are_kings_rook_moved[2] = True

    if board_state[0][0] != 'br':
        are_kings_rook_moved[3] = True
    if board_state[0][4] != 'bK':
        are_kings_rook_moved[4] = True
    if board_state[0][7] != 'br':
        are_kings_rook_moved[5] = True

def king_castle(board_state, piece_pos, are_kings_rook_moved):
    row = piece_pos[0]
    col = piece_pos[1]
    piece = board_state[row][col]
    if piece and piece[1] == 'K':
        if piece[0] == 'w':
            if (row, col) == (7, 6) and board_state[7][7] and board_state[7][7] == 'wr':
                if not (are_kings_rook_moved[1] or are_kings_rook_moved[2]):
                    board_state[7][5] = 'wr'
                    board_state[7][7] = None

            elif (row, col) == (7, 2) and board_state[7][0] and board_state[7][0] == 'wr':
                if not (are_kings_rook_moved[0] or are_kings_rook_moved[1]):
                    board_state[7][3] = 'wr'
                    board_state[7][0] = None

        elif piece[0] == 'b':
            if (row, col) == (0, 6) and board_state[0][7] and board_state[0][7] == 'br':
                if not (are_kings_rook_moved[4] or are_kings_rook_moved[5]):
                    board_state[0][5] = 'br'
                    board_state[0][7] = None

            elif (row, col) == (0, 2) and board_state[0][0] and board_state[0][0] == 'br':
                if not (are_kings_rook_moved[3] or are_kings_rook_moved[4]):
                    board_state[0][3] = 'br'
                    board_state[0][0] = None

    
