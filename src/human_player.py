from src.player import Player

class HumanPlayer(Player):
    def __init__(self, player_id, name, color):
        super().__init__(player_id, name, color)
        self.selected_column = None
    
    def get_move(self, board):
        return self.selected_column
    
    def set_move(self, column):
        self.selected_column = column
    
    def clear_move(self):
        self.selected_column = None