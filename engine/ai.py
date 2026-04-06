from board import SIZE, check_win
import math
import random

AI = "O"
PLAYER = "X"
EMPTY = "."

SCORES = {
    0: 0,
    1: 2,
    2: 20,
    3: 300,
    4: 12000,
    5: 1000000,
}

POSITION = [
    [3, 2, 2, 2, 3],
    [2, 3, 3, 3, 2],
    [2, 3, 5, 3, 2],
    [2, 3, 3, 3, 2],
    [3, 2, 2, 2, 3],
]

def get_lines(board):
    lines = []

    for r in range(SIZE):
        coords = [(r, c) for c in range(SIZE)]
        lines.append(([board[r][c] for c in range(SIZE)], coords))

    for c in range(SIZE):
        coords = [(r, c) for r in range(SIZE)]
        lines.append(([board[r][c] for r in range(SIZE)], coords))

    coords = [(i, i) for i in range(SIZE)]
    lines.append(([board[i][i] for i in range(SIZE)], coords))

    coords = [(i, SIZE - 1 - i) for i in range(SIZE)]
    lines.append(([board[i][SIZE - 1 - i] for i in range(SIZE)], coords))

    return lines

def get_empty(board):
    return [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == EMPTY]

def rand_move(board):
    cells = get_empty(board)
    return random.choice(cells) if cells else (None, None)

def full(board):
    return all(board[r][c] != EMPTY for r in range(SIZE) for c in range(SIZE))

def empty_board(board):
    return all(board[r][c] == EMPTY for r in range(SIZE) for c in range(SIZE))

def score_line(line, ai=AI, opp=PLAYER):
    ai_count = line.count(ai)
    opp_count = line.count(opp)
    empty_count = line.count(EMPTY)

    if ai_count > 0 and opp_count > 0:
        return 0

    if ai_count == 5:
        return 10**9
    if opp_count == 5:
        return -(10**9)

    if ai_count == 4 and empty_count == 1:
        return 25000
    if opp_count == 4 and empty_count == 1:
        return -30000

    if ai_count == 3 and empty_count == 2:
        return 1200
    if opp_count == 3 and empty_count == 2:
        return -1600

    if ai_count == 2 and empty_count == 3:
        return 80
    if opp_count == 2 and empty_count == 3:
        return -100

    if ai_count > 0:
        return SCORES[ai_count]
    if opp_count > 0:
        return -SCORES[opp_count]
    return 0

def pos_score(board, ai=AI, opp=PLAYER):
    score = 0
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == ai:
                score += POSITION[r][c]
            elif board[r][c] == opp:
                score -= POSITION[r][c]
    return score

def count_threats(board, player):
    count = 0
    enemy = PLAYER if player == AI else AI

    for line, _ in get_lines(board):
        p_count = line.count(player)
        e_count = line.count(EMPTY)
        enemy_count = line.count(enemy)

        if enemy_count == 0 and p_count == 3 and e_count == 2:
            count += 1
        if enemy_count == 0 and p_count == 4 and e_count == 1:
            count += 4

    return count

def evaluate(board, ai=AI, opp=PLAYER):
    if check_win(board, ai):
        return 10**9
    if check_win(board, opp):
        return -(10**9)

    total = 0

    for line, _ in get_lines(board):
        total += score_line(line, ai, opp)

    total += pos_score(board, ai, opp)

    ai_threats = count_threats(board, ai)
    opp_threats = count_threats(board, opp)

    total += ai_threats * 3000
    total -= opp_threats * 3800

    return total

def instant_win(board, player):
    for r, c in get_empty(board):
        board[r][c] = player
        if check_win(board, player):
            board[r][c] = EMPTY
            return (r, c)
        board[r][c] = EMPTY
    return None

def basic_moves(board):
    return get_empty(board)

def move_score(board, move):
    r, c = move
    score = POSITION[r][c] * 30

    board[r][c] = AI
    if check_win(board, AI):
        board[r][c] = EMPTY
        return 10**10

    score += evaluate(board)
    score += count_threats(board, AI) * 5000
    board[r][c] = EMPTY

    board[r][c] = PLAYER
    if check_win(board, PLAYER):
        score += 9 * 10**9

    score += count_threats(board, PLAYER) * 6000
    board[r][c] = EMPTY

    return score

def hard_moves(board):
    moves = get_empty(board)
    if not moves:
        return []

    scored = [(move_score(board, move), move) for move in moves]
    scored.sort(reverse=True)

    return [move for _, move in scored[:12]]

def minimax(board, depth, alpha, beta, maximizing, hard=False):
    if check_win(board, AI):
        return 10**9 + depth
    if check_win(board, PLAYER):
        return -(10**9) - depth
    if depth == 0 or full(board):
        return evaluate(board)

    moves = hard_moves(board) if hard else basic_moves(board)

    if maximizing:
        best = -math.inf
        for r, c in moves:
            board[r][c] = AI
            val = minimax(board, depth - 1, alpha, beta, False, hard)
            board[r][c] = EMPTY
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        for r, c in moves:
            board[r][c] = PLAYER
            val = minimax(board, depth - 1, alpha, beta, True, hard)
            board[r][c] = EMPTY
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

def medium_move(board):
    if empty_board(board):
        return rand_move(board)

    block = instant_win(board, PLAYER)
    if block:
        return block

    moves = basic_moves(board)
    if not moves:
        return (None, None)

    best_score = -math.inf
    best_moves = []

    for r, c in moves:
        board[r][c] = AI
        score = minimax(board, 0, -math.inf, math.inf, False, False)
        board[r][c] = EMPTY

        if score > best_score:
            best_score = score
            best_moves = [(r, c)]
        elif score == best_score:
            best_moves.append((r, c))

    return random.choice(best_moves)

def hard_move(board):
    if empty_board(board):
        return rand_move(board)

    win = instant_win(board, AI)
    if win:
        return win

    block = instant_win(board, PLAYER)
    if block:
        return block

    moves = hard_moves(board)
    if not moves:
        return (None, None)

    best_score = -math.inf
    best_moves = []

    for r, c in moves:
        board[r][c] = AI
        score = minimax(board, 2, -math.inf, math.inf, False, True)
        board[r][c] = EMPTY

        if score > best_score:
            best_score = score
            best_moves = [(r, c)]
        elif score == best_score:
            best_moves.append((r, c))

    return random.choice(best_moves)

def best_move(board, difficulty):
    if difficulty == -1:
        return rand_move(board)

    if difficulty == 0:
        return medium_move(board)

    if difficulty == 1:
        return hard_move(board)

    return medium_move(board)