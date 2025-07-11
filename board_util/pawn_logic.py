def get_pawn_taking_moves(board_state, piece_pos):
    out = []
    row = piece_pos[0]
    col = piece_pos[1]
    color = board_state[row][col][0]

    if color == 'w':
        if col > 0 and row > 0 and board_state[row-1][col-1]: # taking left
                if board_state[row-1][col-1][0] == 'b' and board_state[row-1][col-1][1] != 'K': 
                    out.append((row-1,col-1))
        if col < 7 and row > 0 and board_state[row-1][col+1]: # taking right
            if board_state[row-1][col+1][0] == 'b' and board_state[row-1][col+1][1] != 'K': 
                out.append((row-1,col+1))
    else:
        if col > 0 and row < 7 and board_state[row+1][col-1]:  # taking left
            if board_state[row+1][col-1][0] == 'w' and board_state[row+1][col-1][1] != 'K':
                out.append((row+1,col-1))
        if col < 7 and row < 7 and board_state[row+1][col+1]: # taking right
            if board_state[row+1][col+1][0] == 'w' and board_state[row+1][col+1][1] != 'K': 
                out.append((row+1,col+1))
    return out

def get_available_moves_pawn(board_state, piece_pos):
    out = []
    row = piece_pos[0]
    col = piece_pos[1]
    color = board_state[row][col][0]
    if color == 'w':
        if row > 0 and not board_state[row - 1][col]: # move forward one place
            out.append((row - 1, col))
        if row == 6 and not board_state[row-2][col]: # at the beggining
            out.append((row - 2, col))

        #if col > 0 and row > 0 and board_state[row-1][col-1]: # taking left
        #    if board_state[row-1][col-1][0] == 'b' and board_state[row-1][col-1][1] != 'K': 
        #        out.append((row-1,col-1))
        #if col < 7 and row > 0 and board_state[row-1][col+1]: # taking right
        #    if board_state[row-1][col+1][0] == 'b' and board_state[row-1][col+1][1] != 'K': 
        #        out.append((row-1,col+1))

        if row == 3: # en passant
            if col > 0 and board_state[row][col-1]:
                if board_state[row][col-1][0] == 'b' and board_state[row][col-1][1] == 'p':
                    out.append((row-1,col-1))
            
            if col < 7 and board_state[row][col+1]:
                if board_state[row][col+1][0] == 'b' and board_state[row][col+1][1] == 'p':
                    out.append((row-1,col+1))

    else: # for black pieces
        if row < 7 and not board_state[row + 1][col]: # move forward one place
            out.append((row + 1, col))
        if row == 1 and not board_state[row+2][col]: # at the beggining 
            out.append((row + 2, col))

        #if col > 0 and row < 7 and board_state[row+1][col-1]:  # taking left
        #    if board_state[row+1][col-1][0] == 'w' and board_state[row+1][col-1][1] != 'K':
        #        out.append((row+1,col-1))
        #if col < 7 and row < 7 and board_state[row+1][col+1]: # taking right
        #    if board_state[row+1][col+1][0] == 'w' and board_state[row+1][col+1][1] != 'K': 
        #        out.append((row+1,col+1))

        if row == 4: # en passant
            if col > 0 and board_state[row][col-1]:
                if board_state[row][col-1][0] == 'w' and board_state[row][col-1][1] == 'p':
                    out.append((row+1,col-1))
            
            if col < 7 and board_state[row][col+1]:
                if board_state[row][col+1][0] == 'w' and board_state[row][col+1][1] == 'p':
                    out.append((row+1,col+1))
    
    out.extend(get_pawn_taking_moves(board_state, piece_pos))
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
