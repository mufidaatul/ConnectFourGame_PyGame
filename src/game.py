import pygame
import sys
from src.board import Board
from src.human_player import HumanPlayer
from src.ai_player import AIPlayer
from src.constants import (
    MENU, PLAYING, GAME_OVER, PLAYER_1_COLOR, PLAYER_2_COLOR,
    DRAW, PLAYER_1_WIN, PLAYER_2_WIN
)
from src.utils import get_column_from_mouse
from ui.renderer import Renderer
from ui.menu import Menu
from ui.animations import PieceAnimation

class ConnectFourGame:
    def __init__(self, screen):
        """Initialize the Connect Four game"""
        self.screen = screen
        self.board = Board()
        self.renderer = Renderer(screen)
        self.menu = Menu(screen)
        
        self.state = MENU
        self.current_player_index = 0
        self.players = []
        self.game_result = None
        
        self.current_animation = None
        self.animation_delay = 0
        self.mouse_col = None

        # Tambahan: menyimpan move yang tertunda sampai animasi selesai
        self.pending_move = None
    
    def start_game(self, player1_type, player2_type, ai_difficulty=None):
        self.board.reset()
        self.current_player_index = 0
        self.game_result = None
        self.current_animation = None
        self.animation_delay = 0
        self.pending_move = None
        
        self.players = []
        
        if player1_type == "human":
            self.players.append(HumanPlayer(1, "Player 1", PLAYER_1_COLOR))
        else:
            self.players.append(AIPlayer(1, "AI", PLAYER_1_COLOR, ai_difficulty))
        
        if player2_type == "human":
            self.players.append(HumanPlayer(2, "Player 2", PLAYER_2_COLOR))
        else:
            self.players.append(AIPlayer(2, "AI", PLAYER_2_COLOR, ai_difficulty))
        
        self.state = PLAYING
    
    def handle_event(self, event):
        if self.state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = self.menu.handle_click(event.pos)
                if action == "start_human_vs_human":
                    self.start_game("human", "human")
                elif action == "start_human_vs_ai":
                    self.start_game("human", "ai", self.menu.selected_difficulty)
                elif action == "quit":
                    pygame.quit()
                    sys.exit()
        
        elif self.state == PLAYING:
            if event.type == pygame.MOUSEMOTION:
                self.mouse_col = get_column_from_mouse(event.pos[0])
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_animation is None:
                    current_player = self.players[self.current_player_index]
                    if isinstance(current_player, HumanPlayer):
                        col = get_column_from_mouse(event.pos[0])
                        if col is not None and self.board.is_valid_move(col):
                            self._make_move(col)
        
        elif self.state == GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = self.menu.handle_game_over_click(event.pos)
                if action == "play_again":
                    player1_type = "human" if isinstance(self.players[0], HumanPlayer) else "ai"
                    player2_type = "human" if isinstance(self.players[1], HumanPlayer) else "ai"
                    ai_diff = None
                    for player in self.players:
                        if isinstance(player, AIPlayer):
                            ai_diff = player.difficulty
                            break
                    self.start_game(player1_type, player2_type, ai_diff)
                elif action == "main_menu":
                    self.state = MENU
    
    def update(self):
        if self.state == PLAYING:
            if self.current_animation:
                self.current_animation.update()
                if self.current_animation.is_finished:
                    if self.animation_delay > 0:
                        self.animation_delay -= 1
                    else:
                        self._finish_move()
            
            elif self.current_animation is None and self.game_result is None:
                current_player = self.players[self.current_player_index]
                if isinstance(current_player, AIPlayer):
                    col = current_player.get_move(self.board)
                    if col is not None and self.board.is_valid_move(col):
                        self._make_move(col)
    
    def _make_move(self, col):
        """Start animation and store move for later execution"""
        current_player = self.players[self.current_player_index]
        target_row = None
        for row in range(len(self.board.grid) - 1, -1, -1):
            if self.board.grid[row][col] == 0:
                target_row = row
                break
        
        if target_row is not None:
            # Simpan dulu move-nya, baru nanti diproses saat animasi selesai
            self.pending_move = (col, target_row, current_player)
            self.current_animation = PieceAnimation(col, target_row, current_player.color)
            self.animation_delay = 10
    
    def _finish_move(self):
        """Execute stored move after animation and switch turn"""
        self.current_animation = None
        
        if self.pending_move:
            col, _, player = self.pending_move
            self.board.make_move(col, player.player_id)
            self.pending_move = None

        game_state = self.board.get_game_state()
        if game_state is not None:
            self.game_result = game_state
            self.state = GAME_OVER
        else:
            self.current_player_index = 1 - self.current_player_index
    
    def draw(self):
        if self.state == MENU:
            if self.menu.current_menu == "main":
                self.menu.draw_main_menu()
            elif self.menu.current_menu == "difficulty":
                self.menu.draw_difficulty_menu()
        
        elif self.state == PLAYING:
            self.renderer.clear_screen()
            self.renderer.draw_board(self.board)
            
            if (self.current_animation is None and 
                isinstance(self.players[self.current_player_index], HumanPlayer) and
                self.mouse_col is not None):
                self.renderer.draw_preview_piece(
                    self.mouse_col, 
                    self.players[self.current_player_index].color
                )
            
            if self.current_animation:
                from config.settings import BOARD_X
                self.current_animation.draw(self.screen, BOARD_X)
            
            self.renderer.draw_header(
                self.players[self.current_player_index], 
                None
            )
            self.renderer.draw_side_panel(
                self.players[0], 
                self.players[1], 
                self.players[self.current_player_index]
            )
        
        elif self.state == GAME_OVER:
            self.renderer.clear_screen()
            self.renderer.draw_board(self.board)
            self.renderer.draw_header(None, self.game_result)
            self.renderer.draw_side_panel(
                self.players[0], 
                self.players[1], 
                self.players[self.current_player_index]
            )
            
            if self.game_result == DRAW:
                winner_text = "It's a Draw!"
            elif self.game_result == PLAYER_1_WIN:
                winner_text = f"{self.players[0].name} Wins!"
            else:
                winner_text = f"{self.players[1].name} Wins!"
            
            self.menu.draw_game_over(winner_text)
