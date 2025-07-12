def get_pawn_taking_moves(board_state, piece_pos): # gives the taking pos if only piece exists in that cell
    out = []
    row = piece_pos[0]
    col = piece_pos[1]
    color = board_state[row][col][0]

    if color == 'w':
        if col > 0 and row > 0 and board_state[row-1][col-1]: # taking left
            if board_state[row-1][col-1][0] == 'b': 
                out.append((row-1,col-1))
        if col < 7 and row > 0 and board_state[row-1][col+1]: # taking right
            if board_state[row-1][col+1][0] == 'b': 
                out.append((row-1,col+1))
    else:
        if col > 0 and row < 7 and board_state[row+1][col-1]:  # taking left
            if board_state[row+1][col-1][0] == 'w':
                out.append((row+1,col-1))
        if col < 7 and row < 7 and board_state[row+1][col+1]: # taking right
            if board_state[row+1][col+1][0] == 'w': 
                out.append((row+1,col+1))
    return out

def get_pawn_taking_moves_in_every_case(board_state, king_color): # gives cell where king would be in check by pawns
    taking_cells = set()
    for i in range(8):
        for j in range(8):
            piece = board_state[i][j]
            if piece and piece[1] == 'p':
                if piece[0] == 'w' != king_color:
                    taking_cells.add((i-1, j-1))
                    taking_cells.add((i-1, j+1))
                elif piece[0] == 'b' != king_color:
                    taking_cells.add((i+1, j-1))
                    taking_cells.add((i+1, j+1))
    
    remove_cells = set()
    for pair in taking_cells:
        if pair[0] < 0 or pair[0] > 7:
            remove_cells.add(pair)
        if pair[1] < 0 or pair[1] > 7:
            remove_cells.add(pair)  
    
    out = taking_cells - remove_cells
    return out

def get_available_moves_pawn(board_state, piece_pos, are_pawns_moved):
    out = []
    row = piece_pos[0]
    col = piece_pos[1]
    color = board_state[row][col][0]
    if color == 'w':
        if row > 0 and not board_state[row - 1][col]: # move forward one place
            out.append((row - 1, col))
        if row == 6 and not board_state[row-2][col] and not board_state[row-1][col]: # at the beggining
            out.append((row - 2, col))

        if row == 3: # en passant
            if col > 0 and board_state[row][col-1] and not are_pawns_moved[col-1]:
                if board_state[row][col-1][0] == 'b' and board_state[row][col-1][1] == 'p':
                    out.append((row-1,col-1))
            
            if col < 7 and board_state[row][col+1] and not are_pawns_moved[col+1]:
                if board_state[row][col+1][0] == 'b' and board_state[row][col+1][1] == 'p':
                    out.append((row-1,col+1))

    elif color == 'b' and not are_pawns_moved[8 + col]: # for black pieces
        if row < 7 and not board_state[row + 1][col]: # move forward one place
            out.append((row + 1, col))
        if row == 1 and not board_state[row+2][col] and not board_state[row+1][col]: # at the beggining 
            out.append((row + 2, col))

        if row == 4: # en passant
            if col > 0 and board_state[row][col-1] and not are_pawns_moved[col-1]:
                if board_state[row][col-1][0] == 'w' and board_state[row][col-1][1] == 'p':
                    out.append((row+1,col-1))
            
            if col < 7 and board_state[row][col+1] and not are_pawns_moved[col+1]:
                if board_state[row][col+1][0] == 'w' and board_state[row][col+1][1] == 'p':
                    out.append((row+1,col+1))
    
    pawn_taking_lst = get_pawn_taking_moves(board_state, piece_pos)
    for pair in pawn_taking_lst:
        if board_state[pair[0]][pair[1]][1] == 'K':
            pawn_taking_lst.remove(pair)

    out.extend(pawn_taking_lst)
    return out

def en_passant(board_state, piece_pos):
    row = piece_pos[0]
    col = piece_pos[1]
    piece = board_state[row][col]

    if piece and piece[1] == 'p':
        if piece[0] == 'w':
            if board_state[row + 1][col] and board_state[row + 1][col][0] == 'b' and board_state[row + 1][col][1] == 'p':
                board_state[row + 1][col] = None
        else: # for black
            if board_state[row - 1][col] and board_state[row - 1][col][0] == 'w' and board_state[row - 1][col][1] == 'p':
                board_state[row - 1][col] = None

def can_be_promoted(board_state, piece_pos):
    '''
    0 for not promoting
    1 for white promoting
    2 for black promoting
    '''
    row = piece_pos[0]
    col = piece_pos[1]
    piece = board_state[row][col]

    if piece and piece[1] == 'p':
        if piece[0] == 'w' and row == 0:
            return 1
        if piece[0] == 'b' and row == 7:
            return 2
    return 0

def get_promotable_pieces(board_state, piece_pos):
    piece = board_state[piece_pos[0]][piece_pos[1]]
    if piece and piece[1] == 'p':
        if piece[0] == 'w':
            return ('wq', 'wr', 'wk', 'wb')
        elif piece[0] == 'b':
            return ('bq', 'br', 'bk', 'bb')
    return None

def change_state_of_moved_pawns(board_state, are_pawns_moved):
    for i in range(8):
        if board_state[2][i] == 'bp':
            are_pawns_moved[i] = True
        if board_state[5][i] == 'wp':
            are_pawns_moved[8 + i] = True
      
