from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, player_id, name, color):
        self.player_id = player_id
        self.name = name
        self.color = color
    
    @abstractmethod
    def get_move(self, board):
        
        pass
    
    def __str__(self):
        return f"{self.name} (Player {self.player_id})"