def get_available_moves_knight(board_state, piece_pos):
    out = []
    row = piece_pos[0]
    col = piece_pos[1]
    color = board_state[row][col][0]
    remove_items = []

    for i in range(4):
        if i in (0, 3):
            out.append((row + (-1)**i, col + 2*(-1)**i))
            out.append((row + 2*(-1)**i, col + (-1)**i))
        else:
            out.append((row + (-1)**i, col + 2*(-1)**(i+1)))
            out.append((row + 2*(-1)**i, col + (-1)**(i+1)))

    for pair in out:
        flag_removed = False
        if pair[0] < 0 or pair[0] > 7:
            remove_items.append(pair)
            flag_removed = True
        if pair[1] < 0 or pair[1] > 7:
            remove_items.append(pair)
            flag_removed = True
        
        if not flag_removed:
            if board_state[pair[0]][pair[1]] and board_state[pair[0]][pair[1]][1] == 'K':
                remove_items.append(pair)
            if board_state[pair[0]][pair[1]] and board_state[pair[0]][pair[1]][0] == color:
                remove_items.append(pair)

    out = [x for x in out if x not in remove_items]
    return out
        