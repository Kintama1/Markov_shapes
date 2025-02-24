import pygame
import asyncio
from menu_system import WebMenuManager
from game import MarkovGame
from utils.settings import WIDTH, HEIGHT

async def main():
    """
    Main program entry point that coordinates between menu and game states.
    """
    # Initialize pygame
    pygame.init()
    
    # Create screen that will be shared between menu and game
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Markov Shapes")
    
    # Initialize menu system with the shared screen
    menu_manager = WebMenuManager(screen)
    
    # Game state control
    current_state = "menu"
    running = True
    
    while running:
        if current_state == "menu":
            # Draw the current menu
            menu_manager.draw()
            
            # Handle menu events and state transitions
            state_change = await menu_manager.handle_events()
            
            if state_change == "quit":
                running = False
            elif state_change == "game":
                # Get current settings from menu
                settings = menu_manager.get_settings()
                
                # Initialize game with those settings and shared screen
                game = MarkovGame(settings, screen)
                
                # Switch to game state
                current_state = "game"
        
        elif current_state == "game":
            # Run the game - it will return a state when finished
            next_state = await game.run()
            current_state = next_state  # Should be "menu" or "quit"
            
            if current_state == "quit":
                running = False
        
        # Web-specific: yield control back to browser
        await asyncio.sleep(0)
    
    pygame.quit()

# Run the game
if __name__ == "__main__":
    asyncio.run(main())