SIZE = 5


def create_board():
    return [["." for _ in range(SIZE)] for _ in range(SIZE)]


def check_win(board, player):
    # 5x5 board, đủ 5 ô liên tiếp mới thắng
    # Chỉ có 12 line thắng: 5 hàng, 5 cột, 2 chéo lớn
    for r in range(SIZE):
        if all(board[r][c] == player for c in range(SIZE)):
            return True

    for c in range(SIZE):
        if all(board[r][c] == player for r in range(SIZE)):
            return True

    if all(board[i][i] == player for i in range(SIZE)):
        return True

    if all(board[i][SIZE - 1 - i] == player for i in range(SIZE)):
        return True

    return False
