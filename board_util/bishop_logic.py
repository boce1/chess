def get_available_moves_bishop(board_state, piece_pos):
    out = []
    row = piece_pos[0]
    col = piece_pos[1]
    color = board_state[row][col][0]

    temp_row = row
    temp_col = col
    while True: # down right
        if temp_row >= 7 or temp_col >= 7:
            break
        temp_row += 1
        temp_col += 1

        pos = (temp_row, temp_col)
        if board_state[temp_row][temp_col]:
            if board_state[temp_row][temp_col][0] == color:
                break
            if board_state[temp_row][temp_col][1] == 'K':
                break
        out.append(pos)
        if board_state[temp_row][temp_col] and board_state[temp_row][temp_col][0] != color:
            break

    temp_row = row
    temp_col = col
    while True: # down left
        if temp_row >= 7 or temp_col <= 0:
            break
        temp_row += 1
        temp_col -= 1

        pos = (temp_row, temp_col)
        if board_state[temp_row][temp_col]:
            if board_state[temp_row][temp_col][0] == color:
                break
            if board_state[temp_row][temp_col][1] == 'K':
                break
        out.append(pos)
        if board_state[temp_row][temp_col] and board_state[temp_row][temp_col][0] != color:
            break

    temp_row = row
    temp_col = col
    while True: # up left
        if temp_row <= 0 or temp_col <= 0:
            break
        temp_row -= 1
        temp_col -= 1

        pos = (temp_row, temp_col)
        if board_state[temp_row][temp_col]:
            if board_state[temp_row][temp_col][0] == color:
                break
            if board_state[temp_row][temp_col][1] == 'K':
                break
        out.append(pos)
        if board_state[temp_row][temp_col] and board_state[temp_row][temp_col][0] != color:
            break

    temp_row = row
    temp_col = col
    while True: # up right
        if temp_row <= 0 or temp_col >= 7:
            break
        temp_row -= 1
        temp_col += 1

        pos = (temp_row, temp_col)
        if board_state[temp_row][temp_col]:
            if board_state[temp_row][temp_col][0] == color:
                break
            if board_state[temp_row][temp_col][1] == 'K':
                break
        out.append(pos)
        if board_state[temp_row][temp_col] and board_state[temp_row][temp_col][0] != color:
            break
    
    return out