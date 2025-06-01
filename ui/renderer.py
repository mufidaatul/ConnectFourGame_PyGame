import pygame
from src.constants import (
    ROWS, COLS, CELL_SIZE, BLUE, WHITE, CREAM, BLACK, PLAYER_1_COLOR, LIGHT_BROWN,
    PLAYER_2_COLOR, MEDIUM_BROWN, GRAY, LIGHT_GRAY, DARK_BROWN
)
from config.settings import BOARD_X, BOARD_Y, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
from src.utils import create_text_surface

class Renderer:
    def __init__(self, screen):
        """Initialize the renderer"""
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
    
    def draw_board(self, board):
        # Draw board background
        board_rect = pygame.Rect(
            BOARD_X, BOARD_Y, 
            COLS * CELL_SIZE, ROWS * CELL_SIZE
        )
        pygame.draw.rect(self.screen, BLUE, board_rect)
        
        # Draw cells and pieces
        for row in range(ROWS):
            for col in range(COLS):
                # Calculate cell position
                x = BOARD_X + col * CELL_SIZE
                y = BOARD_Y + row * CELL_SIZE
                
                # Draw cell border
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, BLACK, cell_rect, 2)
                
                # Draw piece if exists
                piece = board.grid[row][col]
                if piece != 0:
                    center_x = x + CELL_SIZE // 2
                    center_y = y + CELL_SIZE // 2
                    radius = CELL_SIZE // 2 - 5
                    
                    color = PLAYER_1_COLOR if piece == 1 else PLAYER_2_COLOR
                    pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
                    pygame.draw.circle(self.screen, BLACK, (center_x, center_y), radius, 2)
                else:
                    # Draw empty hole
                    center_x = x + CELL_SIZE // 2
                    center_y = y + CELL_SIZE // 2
                    radius = CELL_SIZE // 2 - 5
                    pygame.draw.circle(self.screen, WHITE, (center_x, center_y), radius)
    
    def draw_preview_piece(self, col, player_color):
        if 0 <= col < COLS:
            x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_Y - CELL_SIZE // 2
            radius = CELL_SIZE // 2 - 5
            
            # Draw semi-transparent preview
            preview_surface = pygame.Surface((radius * 2, radius * 2))
            preview_surface.set_alpha(128)
            pygame.draw.circle(preview_surface, player_color, (radius, radius), radius)
            
            self.screen.blit(preview_surface, (x - radius, y - radius))
    
    def draw_header(self, current_player, game_state):
        header_y = 20
        
        if game_state is None:  # Game in progress
            text = f"{current_player.name}'s Turn"
            color = DARK_BROWN
        elif game_state == 0:  # Draw
            text = "It's a Draw!"
            color = GRAY
        else:  # Someone won
            winner_name = "Player 1" if game_state == 1 else "Player 2"
            text = f"{winner_name} Wins!"
            color = PLAYER_1_COLOR if game_state == 1 else PLAYER_2_COLOR
        
        text_surface = create_text_surface(text, FONT_SIZE_MEDIUM, color)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, header_y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_side_panel(self, player1, player2, current_player):
        panel_x = BOARD_X + COLS * CELL_SIZE + 20
        panel_y = BOARD_Y
        
        # Player 1 info
        p1_text = f"Player 1: {player1.name}"
        p1_surface = create_text_surface(p1_text, FONT_SIZE_SMALL, LIGHT_BROWN)
        self.screen.blit(p1_surface, (panel_x, panel_y))
        
        # Player 2 info
        p2_text = f"Player 2: {player2.name}"
        p2_surface = create_text_surface(p2_text, FONT_SIZE_SMALL, MEDIUM_BROWN)
        self.screen.blit(p2_surface, (panel_x, panel_y + 30))
        
        # Current player indicator
        indicator_y = panel_y + 70
        current_text = "Current:"
        current_surface = create_text_surface(current_text, FONT_SIZE_SMALL, BLACK)
        self.screen.blit(current_surface, (panel_x, indicator_y))
        
        # Draw current player indicator circle
        circle_x = panel_x + current_surface.get_width() + 10
        circle_y = indicator_y + FONT_SIZE_SMALL // 2
        pygame.draw.circle(self.screen, current_player.color, (circle_x, circle_y), 10)
        pygame.draw.circle(self.screen, BLACK, (circle_x, circle_y), 10, 2)
    
    def clear_screen(self, color=CREAM):
        self.screen.fill(color)