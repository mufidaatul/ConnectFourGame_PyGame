"""
Game Settings and Configuration
"""

from src.constants import ROWS, COLS, CELL_SIZE, BOARD_MARGIN

# Screen dimensions
SCREEN_WIDTH = COLS * CELL_SIZE + 2 * BOARD_MARGIN + 200  # Extra space for UI
SCREEN_HEIGHT = ROWS * CELL_SIZE + 2 * BOARD_MARGIN + 200  # Extra space for UI

# Game settings
FPS = 60
GAME_TITLE = "Connect Four"

# Font settings
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 36
FONT_SIZE_SMALL = 24

# UI positions
BOARD_X = BOARD_MARGIN
BOARD_Y = BOARD_MARGIN + 100  # Leave space for header

# Button settings
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20