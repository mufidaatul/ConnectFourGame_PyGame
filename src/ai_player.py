from src.player import Player
from ai.alpha_beta import alpha_beta
from config.difficulty import DIFFICULTY_DEPTHS

class AIPlayer(Player):
    def __init__(self, player_id, name, color, difficulty="easy"):
        super().__init__(player_id, name, color)
        self.difficulty = difficulty
        self.search_depth = DIFFICULTY_DEPTHS.get(difficulty, 3)
    
    def get_move(self, board):
        # Use alpha-beta pruning to find the best move
        _, best_column = alpha_beta(
            board.copy(),
            self.search_depth,
            float('-inf'),
            float('inf'),
            True,
            self.player_id
        )
        
        return best_column
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.search_depth = DIFFICULTY_DEPTHS.get(difficulty, 3)