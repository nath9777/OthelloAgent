import math

def get_opponent(player):
    return "X" if player == "O" else "O"


def is_valid_move(board, player, row, col):
    if board[row][col] != ".":
        return False

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        flipped = False

        while 0 <= r < 12 and 0 <= c < 12 and board[r][c] == get_opponent(player):
            r, c = r + dr, c + dc
            flipped = True

        if 0 <= r < 12 and 0 <= c < 12 and board[r][c] == player and flipped:
            return True

    return False


def make_move(board, player, row, col):
    """
    if not is_valid_move(board, player, row, col):
        raise ValueError("Invalid move")"""

    board[row] = board[row][:col] + player + board[row][col + 1 :]

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        flipped = False

        while 0 <= r < 12 and 0 <= c < 12 and board[r][c] == get_opponent(player):
            r, c = r + dr, c + dc
            flipped = True

        if 0 <= r < 12 and 0 <= c < 12 and board[r][c] == player and flipped:
            r, c = row + dr, col + dc
            while 0 <= r < 12 and 0 <= c < 12 and board[r][c] == get_opponent(player):
                board[r] = board[r][:c] + player + board[r][c + 1 :]
                r, c = r + dr, c + dc


def evaluate_board(board, player):
    score = 0
    for row in board:
        score += row.count(player)
        score -= row.count(get_opponent(player))
    return score


def get_possible_moves(board, player):
    moves = []
    for i in range(12):
        for j in range(12):
            if is_valid_move(board, player, i, j):
                moves.append((i, j))
    return moves


def minimax(board, player, depth, alpha, beta):
    if depth == 0:
        return evaluate_board(board, player)

    possible_moves = get_possible_moves(board, player)

    if not possible_moves:
        return evaluate_board(board, player)

    if player == "O":
        max_eval = -math.inf
        for move in possible_moves:
            new_board = [row[:] for row in board]
            make_move(new_board, player, move[0], move[1])
            eval = minimax(new_board, get_opponent(player), depth - 1, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in possible_moves:
            new_board = [row[:] for row in board]
            make_move(new_board, player, move[0], move[1])
            eval = minimax(new_board, get_opponent(player), depth - 1, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def choose_best_move(board, player):
    possible_moves = get_possible_moves(board, player)

    if possible_moves:
        best_move = possible_moves[0]
        best_score = -math.inf

        for move in possible_moves:
            new_board = [row[:] for row in board]
            make_move(new_board, player, move[0], move[1])
            score = minimax(
                new_board, get_opponent(player), lookahead_depth, -math.inf, math.inf
            )
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
    else:
        return None


def play_game():
    with open("input.txt", "r") as input_file:
        player = input_file.readline().strip()
        input_file.readline()  # Skipping time information
        board = [input_file.readline().strip() for _ in range(12)]

    while True:
        print(f"INPUT for player:\n{player}")
        print("\n".join(board))
        print("##### #####")

        best_move = choose_best_move(board, player)

        if best_move is None:
            break

        make_move(board, player, best_move[0], best_move[1])

        with open("input.txt", "w") as input_file:
            input_file.write(f"{player}\n")
            input_file.write("dummy \n")
            input_file.write("\n".join(board))

        with open("output.txt", "w") as output_file:
            output_file.write(f"{chr(best_move[1] + ord('a'))}{best_move[0] + 1}\n")

        player = get_opponent(player)

    # Game over test
    score_O = evaluate_board(board, "O") + 1
    score_X = evaluate_board(board, "X")

    if score_O > score_X:
        print("Player O wins!")
    elif score_X > score_O:
        print("Player X wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    lookahead_depth = 20  
    play_game()
