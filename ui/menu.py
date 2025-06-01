import pygame
from src.constants import WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, RED, BLUE, YELLOW
from config.settings import (
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING, 
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
)
from config.difficulty import EASY, HARD, DIFFICULTY_DESCRIPTIONS
from src.utils import create_text_surface, create_button, is_point_in_rect

class Menu:
    def __init__(self, screen):
        """Initialize the menu system"""
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Menu state
        self.current_menu = "main"
        self.selected_difficulty = EASY
        
        # Button rectangles
        self.buttons = self._create_buttons()
    
    def _create_buttons(self):
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        return {
            "vs_human": pygame.Rect(center_x - BUTTON_WIDTH // 2, center_y - 80, BUTTON_WIDTH, BUTTON_HEIGHT),
            "vs_ai": pygame.Rect(center_x - BUTTON_WIDTH // 2, center_y, BUTTON_WIDTH, BUTTON_HEIGHT),
            "quit": pygame.Rect(center_x - BUTTON_WIDTH // 2, center_y + 80, BUTTON_WIDTH, BUTTON_HEIGHT),

            "easy": pygame.Rect(center_x - BUTTON_WIDTH // 2, center_y - 30, BUTTON_WIDTH, BUTTON_HEIGHT),
            "hard": pygame.Rect(center_x - BUTTON_WIDTH // 2, center_y + 50, BUTTON_WIDTH, BUTTON_HEIGHT),
            "back": pygame.Rect(center_x - BUTTON_WIDTH // 2, center_y + 130, BUTTON_WIDTH, BUTTON_HEIGHT),

            "play_again": pygame.Rect(center_x - BUTTON_WIDTH // 2, center_y - 20, BUTTON_WIDTH, BUTTON_HEIGHT),
            "main_menu": pygame.Rect(center_x - BUTTON_WIDTH // 2, center_y + 60, BUTTON_WIDTH, BUTTON_HEIGHT)
        }
    
    def _draw_gradient_background(self, color1, color2):
        """Draw vertical gradient background"""
        for y in range(self.screen_height):
            color = [
                color1[i] + (color2[i] - color1[i]) * y // self.screen_height
                for i in range(3)
            ]
            pygame.draw.line(self.screen, color, (0, y), (self.screen_width, y))

    def draw_main_menu(self):
        self._draw_gradient_background((255, 255, 255), (200, 220, 255))
        
        # Title
        title_surface = create_text_surface("Connect Four", FONT_SIZE_LARGE, BLUE)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 120))
        self.screen.blit(title_surface, title_rect)
        
        # Buttons
        self._draw_button("vs_human", "Player vs Player")
        self._draw_button("vs_ai", "Player vs AI")
        self._draw_button("quit", "Quit")
    
    def draw_difficulty_menu(self):
        self._draw_gradient_background((255, 255, 255), (255, 240, 220))
        
        # Title
        title_surface = create_text_surface("Select Difficulty", FONT_SIZE_LARGE, RED)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Easy button
        easy_color = YELLOW if self.selected_difficulty == EASY else LIGHT_GRAY
        self._draw_button("easy", "Easy", fill_color=easy_color)
        
        easy_desc = create_text_surface(DIFFICULTY_DESCRIPTIONS[EASY], FONT_SIZE_SMALL, GRAY)
        easy_desc_rect = easy_desc.get_rect(center=(self.screen_width // 2, self.buttons["easy"].bottom + 20))
        self.screen.blit(easy_desc, easy_desc_rect)
        
        # Hard button
        hard_color = YELLOW if self.selected_difficulty == HARD else LIGHT_GRAY
        self._draw_button("hard", "Hard", fill_color=hard_color)
        
        hard_desc = create_text_surface(DIFFICULTY_DESCRIPTIONS[HARD], FONT_SIZE_SMALL, GRAY)
        hard_desc_rect = hard_desc.get_rect(center=(self.screen_width // 2, self.buttons["hard"].bottom + 20))
        self.screen.blit(hard_desc, hard_desc_rect)
        
        # Back button
        self._draw_button("back", "Back")
    
    def draw_game_over(self, winner_text):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game over box
        box_rect = pygame.Rect(
            self.screen_width // 2 - 200, self.screen_height // 2 - 150,
            400, 300
        )
        pygame.draw.rect(self.screen, LIGHT_GRAY, box_rect, border_radius=20)
        pygame.draw.rect(self.screen, DARK_GRAY, box_rect, 3, border_radius=20)
        
        # Winner text
        winner_surface = create_text_surface(winner_text, FONT_SIZE_LARGE, RED)
        winner_rect = winner_surface.get_rect(center=(self.screen_width // 2, box_rect.top + 70))
        self.screen.blit(winner_surface, winner_rect)
        
        # Buttons
        self._draw_button("play_again", "Play Again")
        self._draw_button("main_menu", "Main Menu")
    
    def _draw_button(self, key, text, fill_color=LIGHT_GRAY):
        rect = self.buttons[key]
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        
        color = DARK_GRAY if is_hovered else fill_color
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=10)
        
        text_surface = create_text_surface(text, FONT_SIZE_MEDIUM, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def handle_click(self, pos):
        if self.current_menu == "main":
            if is_point_in_rect(pos, self.buttons["vs_human"]):
                return "start_human_vs_human"
            elif is_point_in_rect(pos, self.buttons["vs_ai"]):
                self.current_menu = "difficulty"
                return None
            elif is_point_in_rect(pos, self.buttons["quit"]):
                return "quit"
        
        elif self.current_menu == "difficulty":
            if is_point_in_rect(pos, self.buttons["easy"]):
                self.selected_difficulty = EASY
                return "start_human_vs_ai"
            elif is_point_in_rect(pos, self.buttons["hard"]):
                self.selected_difficulty = HARD
                return "start_human_vs_ai"
            elif is_point_in_rect(pos, self.buttons["back"]):
                self.current_menu = "main"
                return None
        
        return None
    
    def handle_game_over_click(self, pos):
        if is_point_in_rect(pos, self.buttons["play_again"]):
            return "play_again"
        elif is_point_in_rect(pos, self.buttons["main_menu"]):
            self.current_menu = "main"
            return "main_menu"
        return None
    
    def reset_to_main(self):
        self.current_menu = "main"
