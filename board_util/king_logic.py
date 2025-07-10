from .pawn_logic import get_available_moves_pawn
from .knight_logic import get_available_moves_knight
from .queen_logic import get_available_moves_queen
from .bishop_logic import get_available_moves_bishop
from .rook_logic import get_available_moves_rook

def get_pos_where_check(board_state, piece_pos):
    out = []
    for i in range(8):
        for j in range(8):
            if (board_state[i][j] and 
                board_state[i][j][0] != board_state[piece_pos[0]][piece_pos[1]][0]):
                opp_piece = board_state[i][j][1]
                pos = (i, j)
                if opp_piece == 'p':
                    moves = get_available_moves_pawn(board_state, pos)
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
                out.extend(moves)
    return out

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
    for i in range(8):
        for j in range(8):
            if board_state[i][j] and board_state[i][j][0] != color and board_state[i][j][1] == 'K':
                oposite_king_pos = (i, j)

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
    out = [x for x in out if not (x in get_pos_where_check(board_state, piece_pos))]
    return out
