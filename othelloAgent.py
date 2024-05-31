import numpy as np

DEPTH = 5
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

def fetch_opponent(p):
    return "X" if p == "O" else "O"

def check_valid(board, p, row, col):
    if board[row, col] != ".":
        return False    

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        flipped = False

        while 0 <= r < 12 and 0 <= c < 12 and board[r, c] == fetch_opponent(p):
            r, c = r + dr, c + dc
            flipped = True

        if 0 <= r < 12 and 0 <= c < 12 and board[r, c] == p and flipped:
            return True

    return False


def move_piece(board, p, row, col):
    board[row, col] = p

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        flipped = False

        while 0 <= r < 12 and 0 <= c < 12 and board[r, c] == fetch_opponent(p):
            r, c = r + dr, c + dc
            flipped = True

        if 0 <= r < 12 and 0 <= c < 12 and board[r, c] == p and flipped:
            r, c = row + dr, col + dc
            while 0 <= r < 12 and 0 <= c < 12 and board[r, c] == fetch_opponent(p):
                board[r, c] = p
                r, c = r + dr, c + dc


def scoring(board, p):    
    score=0
    inter, exter = 0,0
    for i in range(0,12):
        for j in range(0,12):                        
            if (board[i, j] != p):
                continue            
            elif (i==0 and (j==0 or j==11)) or (i==11 and (j==0 or j==11)):                
                score+=3
            elif i==0 or i==11 or j==0 or j==11:                
                score+=2
            else:                 
                flag = False
                for di, dj in DIRECTIONS:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 12 and 0 <= nj < 12:
                        if board[ni, nj] == '.':
                            exter += 1
                            flag=True
                            break                        
                if not flag:
                    inter+=1
                    
    score += (inter - exter)    
    return score

def fin_scoring(board, p):
    return np.count_nonzero(board == p) - np.count_nonzero(board == fetch_opponent(p))


def get_moves(board, p):
    moves = []
    for i in range(12):
        for j in range(12):
            if check_valid(board, p, i, j):
                moves.append((i, j))
    return moves


def minimaxalphabeta(board, p, Global_p, alpha, beta, depth, is_maximizing, passes):
    if depth == 0:
        return scoring(board, Global_p)
    gpm = get_moves(board, p)
    
    if is_maximizing:
        value = float("-inf")
        if not gpm:
            if passes==1:
                fvalue = fin_scoring(board, Global_p)     
                if  fvalue <= 0:
                    return -2000
                else:
                    return fvalue
            elif passes==0:
                passes+=1
            value = minimaxalphabeta(board, fetch_opponent(p), Global_p, alpha, beta, depth - 1, False, passes)
        else:
            passes=0
            for move in gpm:
                row, col = move
                new_board = board.copy()
                move_piece(new_board, p, row, col)
                value = max(
                    value,
                    minimaxalphabeta(
                        new_board,
                        fetch_opponent(p),
                        Global_p,
                        alpha,
                        beta,
                        depth - 1,
                        False,
                        passes
                    ),
                )
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        return value
    else:
        value = float("inf")
        if not gpm:
            if passes==1:
                fvalue = fin_scoring(board, Global_p)     
                if  fvalue <= 0:
                    return -2000
                else:
                    return fvalue
            elif passes==0:
                passes+=1
            value = minimaxalphabeta(board, fetch_opponent(p), Global_p, alpha, beta, depth - 1, True, passes)
            
        else:
            passes=0
            for move in gpm:
                row, col = move
                new_board = board.copy()
                move_piece(new_board, p, row, col)
                value = min(
                    value,
                    minimaxalphabeta(
                        new_board,
                        fetch_opponent(p),
                        Global_p,
                        alpha,
                        beta,
                        depth - 1,
                        True,
                        passes
                    ),
                )
                beta = min(beta, value)
                if beta <= alpha:
                    break
        return value


def move_choice(board, p, Global_p, depth=DEPTH):
    fin_score = float("-inf")
    fin_move = None
    gpm = get_moves(board, p)

    for move in gpm:
        row, col = move
        new_board = board.copy()
        move_piece(new_board, p, row, col)
        passes=0
        score = minimaxalphabeta(
            new_board,
            fetch_opponent(p),
            Global_p,
            float("-inf"),
            float("inf"),
            depth - 1,
            False,
            passes
        )

        if score > fin_score:
            fin_score = score
            fin_move = move

    return fin_move



def reversi_run():
        
    with open("input.txt", "r") as input_file:
        p = input_file.readline().strip()
        left_time, _ = map(float, input_file.readline().split())
        board = np.array([list(input_file.readline().strip()) for _ in range(12)])

    Global_p = p
    if left_time > 150:
        depth = DEPTH
    elif left_time > 60:
        depth = DEPTH - 1
    else:
        depth = DEPTH - 2

    while True:
        print(f"INPUT for player:\n{p}")
        print("\n".join(board))
        print("##### #####")

        fin_move = move_choice(board, p, Global_p, depth)
        
        if fin_move is None:
            break

        if fin_move is not None:        
            with open("output.txt", "w") as output_file:
                output_file.write(f"{chr(fin_move[1] + ord('a'))}{fin_move[0] + 1}\n")


        p = fetch_opponent(p)

    # Game over test
    score_O = fin_scoring(board, "O") + 1
    score_X = fin_scoring(board, "X")

    if score_O > score_X:
        print("Player O wins!")
    elif score_X > score_O:
        print("Player X wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    reversi_run()