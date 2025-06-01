from src.constants import ROWS, COLS

def evaluate_board(board, player_id):
    """
    Evaluate the board from the perspective of the given player
    
    Args:
        board (Board): Board to evaluate
        player_id (int): Player ID (1 or 2)
    
    Returns:
        int: Board evaluation score
    """
    opponent_id = 2 if player_id == 1 else 1
    
    # Check for immediate win/loss
    winner = board.check_winner()
    if winner == player_id:
        return 10000
    elif winner == opponent_id:
        return -10000
    
    score = 0
    
    # Evaluate all possible 4-in-a-row combinations
    score += evaluate_all_windows(board.grid, player_id)
    
    # Center column preference
    center_col = COLS // 2
    center_count = sum(1 for row in range(ROWS) if board.grid[row][center_col] == player_id)
    score += center_count * 3
    
    return score

def evaluate_all_windows(grid, player_id):
    """Evaluate all 4-cell windows on the board"""
    score = 0
    opponent_id = 2 if player_id == 1 else 1
    
    # Horizontal windows
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = [grid[row][col + i] for i in range(4)]
            score += evaluate_window(window, player_id, opponent_id)
    
    # Vertical windows
    for row in range(ROWS - 3):
        for col in range(COLS):
            window = [grid[row + i][col] for i in range(4)]
            score += evaluate_window(window, player_id, opponent_id)
    
    # Diagonal windows (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [grid[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, player_id, opponent_id)
    
    # Diagonal windows (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            window = [grid[row + i][col - i] for i in range(4)]
            score += evaluate_window(window, player_id, opponent_id)
    
    return score

def evaluate_window(window, player_id, opponent_id):
    """Evaluate a 4-cell window"""
    score = 0
    player_count = window.count(player_id)
    opponent_count = window.count(opponent_id)
    empty_count = window.count(0)
    
    # If opponent has pieces in window, we can't use it
    if opponent_count > 0 and player_count > 0:
        return 0
    
    # Score based on our pieces
    if player_count == 4:
        score += 100
    elif player_count == 3 and empty_count == 1:
        score += 10
    elif player_count == 2 and empty_count == 2:
        score += 2
    
    # Penalize opponent opportunities
    if opponent_count == 3 and empty_count == 1:
        score -= 80
    elif opponent_count == 2 and empty_count == 2:
        score -= 10
    
    return score