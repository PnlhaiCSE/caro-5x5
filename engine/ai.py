from board import SIZE, check_win
import math
import random

AI = "O"
HUMAN = "X"
EMPTY = "."

DIFFICULTY_DEPTH = {
    -1: 0,   # dễ
     0: 4,   # trung bình
     1: 8    # khó
}

SCORES = {
    0: 0,
    1: 2,
    2: 20,
    3: 200,
    4: 5000,
    5: 1000000,
}

POSITION = [
    [3, 2, 2, 2, 3],
    [2, 2, 2, 2, 2],
    [2, 2, 4, 2, 2],
    [2, 2, 2, 2, 2],
    [3, 2, 2, 2, 3],
]


def get_winning_lines(board):
    lines = []

    for r in range(SIZE):
        lines.append(([board[r][c] for c in range(SIZE)], [(r, c) for c in range(SIZE)]))

    for c in range(SIZE):
        lines.append(([board[r][c] for r in range(SIZE)], [(r, c) for r in range(SIZE)]))

    lines.append(([board[i][i] for i in range(SIZE)], [(i, i) for i in range(SIZE)]))
    lines.append(([board[i][SIZE - 1 - i] for i in range(SIZE)], [(i, SIZE - 1 - i) for i in range(SIZE)]))

    return lines


def score_line(line, ai=AI, opp=HUMAN):
    ai_count = line.count(ai)
    opp_count = line.count(opp)

    if ai_count > 0 and opp_count > 0:
        return 0
    if ai_count > 0:
        return SCORES[ai_count]
    if opp_count > 0:
        return -SCORES[opp_count]
    return 0


def position_score(board, ai=AI, opp=HUMAN):
    score = 0
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == ai:
                score += POSITION[r][c]
            elif board[r][c] == opp:
                score -= POSITION[r][c]
    return score


def evaluate(board, ai=AI, opp=HUMAN):
    if check_win(board, ai):
        return 10**9
    if check_win(board, opp):
        return -(10**9)

    line_score = sum(score_line(line, ai, opp) for line, _ in get_winning_lines(board))
    return line_score + position_score(board, ai, opp)


def get_moves(board):
    empties = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == EMPTY]
    if not empties:
        return []

    # opening: ưu tiên giữa nếu còn trống
    center = (SIZE // 2, SIZE // 2)
    if len(empties) == SIZE * SIZE and center in empties:
        return [center]

    # move ordering: ô nào nằm trên nhiều line còn sống thì ưu tiên hơn
    def move_priority(move):
        r, c = move
        score = POSITION[r][c]
        for line, coords in get_winning_lines(board):
            if (r, c) in coords:
                ai_count = line.count(AI)
                opp_count = line.count(HUMAN)
                if ai_count > 0 and opp_count > 0:
                    continue
                score += 100 + max(ai_count, opp_count) * 50
        return score

    # chỉ giữ các ô còn nằm trong ít nhất 1 line chưa chết
    candidates = []
    for move in empties:
        r, c = move
        useful = False
        for line, coords in get_winning_lines(board):
            if (r, c) in coords:
                ai_count = line.count(AI)
                opp_count = line.count(HUMAN)
                if not (ai_count > 0 and opp_count > 0):
                    useful = True
                    break
        if useful:
            candidates.append(move)

    if not candidates:
        candidates = empties

    candidates.sort(key=move_priority, reverse=True)
    return candidates


def is_full(board):
    return all(board[r][c] != EMPTY for r in range(SIZE) for c in range(SIZE))


def minimax(board, depth, alpha, beta, maximizing):
    if check_win(board, AI):
        return 10**9 + depth
    if check_win(board, HUMAN):
        return -(10**9) - depth
    if depth == 0 or is_full(board):
        return evaluate(board)

    moves = get_moves(board)

    if maximizing:
        best = -math.inf
        for r, c in moves:
            board[r][c] = AI
            val = minimax(board, depth - 1, alpha, beta, False)
            board[r][c] = EMPTY
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        for r, c in moves:
            board[r][c] = HUMAN
            val = minimax(board, depth - 1, alpha, beta, True)
            board[r][c] = EMPTY
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def best_move(board, difficulty=0):
    moves = get_moves(board)
    if not moves:
        return None, None

    # easy: random trong top move hợp lý
    if difficulty == -1:
        top = moves[: min(5, len(moves))]
        return random.choice(top)

    depth = DIFFICULTY_DEPTH.get(difficulty, 4)
    best_score = -math.inf
    best = moves[0]

    for r, c in moves:
        board[r][c] = AI
        score = minimax(board, depth - 1, -math.inf, math.inf, False)
        board[r][c] = EMPTY

        if score > best_score:
            best_score = score
            best = (r, c)

    return best
