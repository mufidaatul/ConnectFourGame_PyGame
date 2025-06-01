import numpy as np
from src.constants import ROWS, COLS, DRAW, PLAYER_1_WIN, PLAYER_2_WIN

class Board:
    def __init__(self):
        self.grid = np.zeros((ROWS, COLS), dtype=int)
        self.last_move = None
    
    def reset(self):
        self.grid = np.zeros((ROWS, COLS), dtype=int)
        self.last_move = None
    
    def is_valid_move(self, col):
        # Valid jika kolom di dalam batas dan paling atas kolom kosong
        return 0 <= col < COLS and self.grid[0][col] == 0
    
    def get_valid_moves(self):
        return [col for col in range(COLS) if self.is_valid_move(col)]
    
    def make_move(self, col, player):
        if not self.is_valid_move(col):
            return False
        
        # Cari baris terendah kosong di kolom tersebut
        for row in range(ROWS - 1, -1, -1):
            if self.grid[row][col] == 0:
                self.grid[row][col] = player
                self.last_move = (row, col)
                return True
        
        return False
    
    def undo_move(self, col):
        # Cari pion teratas di kolom dan hapus
        for row in range(ROWS):
            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                break
    
    def check_winner(self):
        # Check horizontal
        for row in range(ROWS):
            for col in range(COLS - 3):
                if (self.grid[row][col] != 0 and
                    self.grid[row][col] == self.grid[row][col + 1] ==
                    self.grid[row][col + 2] == self.grid[row][col + 3]):
                    return self.grid[row][col]
        
        # Check vertical
        for row in range(ROWS - 3):
            for col in range(COLS):
                if (self.grid[row][col] != 0 and
                    self.grid[row][col] == self.grid[row + 1][col] ==
                    self.grid[row + 2][col] == self.grid[row + 3][col]):
                    return self.grid[row][col]
        
        # Check diagonal (top-left to bottom-right)
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if (self.grid[row][col] != 0 and
                    self.grid[row][col] == self.grid[row + 1][col + 1] ==
                    self.grid[row + 2][col + 2] == self.grid[row + 3][col + 3]):
                    return self.grid[row][col]
        
        # Check diagonal (top-right to bottom-left)
        for row in range(ROWS - 3):
            for col in range(3, COLS):
                if (self.grid[row][col] != 0 and
                    self.grid[row][col] == self.grid[row + 1][col - 1] ==
                    self.grid[row + 2][col - 2] == self.grid[row + 3][col - 3]):
                    return self.grid[row][col]
        
        return 0  # No winner
    
    def is_full(self):
        """Check if the board is full (tidak ada 0 sama sekali)"""
        return np.all(self.grid != 0)
    
    def get_game_state(self):
        winner = self.check_winner()
        if winner == 1:
            return PLAYER_1_WIN
        elif winner == 2:
            return PLAYER_2_WIN
        elif self.is_full():
            return DRAW
        else:
            return None  # Game continues
    
    def copy(self):
        new_board = Board()
        new_board.grid = self.grid.copy()
        new_board.last_move = self.last_move
        return new_board
    
    def __str__(self):
        return str(self.grid)
