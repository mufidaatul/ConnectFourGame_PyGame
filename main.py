import pygame
import sys
from src.game import ConnectFourGame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Connect Four")
    clock = pygame.time.Clock()
    
    # Create game instance
    game = ConnectFourGame(screen)
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)
        
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()