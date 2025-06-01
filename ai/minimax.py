import random
from ai.evaluation import evaluate_board

def minimax(board, depth, maximizing_player, player_id):
    """
    Minimax algorithm with limited depth
    
    Args:
        board (Board): Current board state
        depth (int): Maximum search depth
        maximizing_player (bool): True if maximizing, False if minimizing
        player_id (int): AI player ID
    
    Returns:
        tuple: (best_score, best_column)
    """
    valid_moves = board.get_valid_moves()
    
    # Terminal node conditions
    winner = board.check_winner()
    if winner == player_id:
        return (10000 + depth, None)
    elif winner != 0:
        return (-10000 - depth, None)
    elif board.is_full() or depth == 0:
        return (evaluate_board(board, player_id), None)
    
    if maximizing_player:
        max_eval = float('-inf')
        best_col = random.choice(valid_moves)  # Random tie-breaking
        
        for col in valid_moves:
            board.make_move(col, player_id)
            eval_score, _ = minimax(board, depth - 1, False, player_id)
            board.undo_move(col)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_col = col
        
        return (max_eval, best_col)
    
    else:
        min_eval = float('inf')
        best_col = random.choice(valid_moves)  # Random tie-breaking
        opponent_id = 2 if player_id == 1 else 1
        
        for col in valid_moves:
            board.make_move(col, opponent_id)
            eval_score, _ = minimax(board, depth - 1, True, player_id)
            board.undo_move(col)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_col = col
        
        return (min_eval, best_col)