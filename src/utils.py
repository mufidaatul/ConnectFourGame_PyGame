import pygame
from src.constants import COLS, CELL_SIZE
from config.settings import BOARD_X

def get_column_from_mouse(mouse_x):
    if mouse_x < BOARD_X:
        return None
    
    col = (mouse_x - BOARD_X) // CELL_SIZE
    return col if 0 <= col < COLS else None

def create_text_surface(text, font_size, color, font_name=None):
    font = pygame.font.Font(font_name, font_size)
    return font.render(text, True, color)

def create_button(surface, rect, text, font_size, text_color, bg_color, border_color=None):
    pygame.draw.rect(surface, bg_color, rect)
    
    if border_color:
        pygame.draw.rect(surface, border_color, rect, 2)
    
    text_surface = create_text_surface(text, font_size, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def is_point_in_rect(point, rect):
    return rect.collidepoint(point)