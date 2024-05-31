# OthelloAgent
The repository contains code for a Custom Othello Game Playing Agent using heuristics for optimal game-playing performance.


**# Setup**
In this project, we define a new game that we call Duo-Othello. It is similar to the classic game of Reversi / Othello, which is explained below, but with three twists:
1) We play on a 12x12 board instead of the standard 8x8 Reversi board.
2) The start state has 8 pieces on the board instead of the standard 4 pieces.
3) Once the game is over, which is when neither player can place new pieces on the board anymore, the winner is determined by counting the pieces of each color.
4) To mitigate the first-player advantage, the second player is given a bonus of +1. In case of ties (equal scores for both players after bonus), the winner is the one with the most time remaining.
     If the remaining times are equal, the winner is the player that started second)




**# MinMax Alpha Beta Pruning Logic Implemented**
Parameters: The function takes in the current game board, the current player, a global player context, alpha and beta values for pruning, the search depth, a boolean indicating if the current player is maximizing, and a count of consecutive passes.

Base Case: If the maximum search depth is reached, it returns a heuristic score for the board.

Get Moves: It retrieves all possible legal moves for the current player.

Maximizing Player Logic:
1. If there are no moves and it’s the second consecutive pass, it returns a special score.
2. If it’s the first pass, it increments the pass count and recursively calls the function for the opponent.
3. If moves are available, it simulates each move, calls the function recursively for the opponent, updates alpha, and prunes branches where beta <= alpha.

Minimizing Player Logic:
Similar to the maximizing player logic but focuses on minimizing the score.
Updates beta and prunes branches where beta <= alpha.

Alpha-Beta Pruning: This technique is used to eliminate branches in the game tree that don’t need to be explored, improving efficiency by not exploring moves that won't be chosen.


# Heuristic /Evaluation Function
* This heuristic considers both the positional value of the player's pieces and their interaction with empty spaces. 
> Positional Advantage: Pieces in the corners and edges are scored higher because they are generally more advantageous positions.
> Piece Interaction: I take a difference between External pieces (adjacent to empty spaces) and Internal pieces (surrounded by other pieces) to give a higher weightage to moves with more empty spaces adjacent.
> Combining these 2 gives a comprehensive heuristic.

