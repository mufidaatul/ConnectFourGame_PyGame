import pygame
from src.constants import DROP_SPEED, CELL_SIZE
from config.settings import BOARD_Y

class PieceAnimation:
    def __init__(self, col, target_row, color):
        self.col = col
        self.target_row = target_row
        self.color = color
        self.current_y = BOARD_Y - CELL_SIZE  # Start above the board
        self.target_y = BOARD_Y + target_row * CELL_SIZE
        self.is_finished = False
    
    def update(self):
        if not self.is_finished:
            self.current_y += DROP_SPEED
            if self.current_y >= self.target_y:
                self.current_y = self.target_y
                self.is_finished = True
    
    def draw(self, surface, board_x):
        if not self.is_finished or abs(self.current_y - self.target_y) < 5:
            x = board_x + self.col * CELL_SIZE + CELL_SIZE // 2
            y = self.current_y + CELL_SIZE // 2
            radius = CELL_SIZE // 2 - 5
            pygame.draw.circle(surface, self.color, (int(x), int(y)), radius)