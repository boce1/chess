def find_king_pos(board_state, color):
    for i in range(8):
        for j in range(8):
            if board_state[i][j] and board_state[i][j][0] == color and board_state[i][j][1] == 'K':
                return (i, j)
    return None