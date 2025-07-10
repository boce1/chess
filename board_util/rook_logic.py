def get_available_moves_rook(board_state, piece_pos):
    out = []
    row = piece_pos[0]
    col = piece_pos[1]
    color = board_state[row][col][0]
    
    row_temp = row
    while True: # down direction
        if row_temp >= 7:
            break
        row_temp += 1
        pos = (row_temp, col)
        if board_state[row_temp][col]:
            if board_state[row_temp][col][0] == color:
                break
            if board_state[row_temp][col][1] == 'K':
                break
        out.append(pos)
        if board_state[row_temp][col] and board_state[row_temp][col][0] != color:
            break
        
    row_temp = row
    while True: # up direction
        if row_temp <= 0:
            break
        row_temp -= 1
        pos = (row_temp, col)
        if board_state[row_temp][col]:
            if board_state[row_temp][col][0] == color:
                break
            if board_state[row_temp][col][1] == 'K':
                break
        out.append(pos)
        if board_state[row_temp][col] and board_state[row_temp][col][0] != color:
            break

    col_temp = col
    while True:
        if col_temp >= 7:
            break
        col_temp += 1
        pos = (row, col_temp)
        if board_state[row][col_temp]:
            if board_state[row][col_temp][0] == color:
                break
            if board_state[row][col_temp][1] == 'K':
                break
        out.append(pos)
        if board_state[row][col_temp] and board_state[row][col_temp][0] != color:
            break

    col_temp = col
    while True:
        if col_temp <= 0:
            break
        col_temp -= 1
        pos = (row, col_temp)
        if board_state[row][col_temp]:
            if board_state[row][col_temp][0] == color:
                break
            if board_state[row][col_temp][1] == 'K':
                break
        out.append(pos)
        if board_state[row][col_temp] and board_state[row][col_temp][0] != color:
            break

    return out
        