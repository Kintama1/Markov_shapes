import pygame
import time
from markov import MarkovShape
import asyncio
from utils.settings import GameSettings, WIDTH, HEIGHT, FPS, CONTROLS
from utils.button import Button

class MarkovGame:
    def __init__(self, settings: GameSettings, screen=None):
        self.settings = settings
        self.width = WIDTH
        self.height = HEIGHT
        
        # Use provided screen or create one if not provided
        if screen is None:
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Markov Shapes")
        else:
            self.screen = screen
        
        self.shapes = MarkovShape(settings.shapes_matrix)
        self.shapes_list = self.shapes.shape_sequence(length=settings.num_shapes)
        self.shape_idx = 0
        self.current_shape = self.shapes_list[self.shape_idx]
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.game_over = False
        
        # Initialize shape position
        self.shape_rect = pygame.Rect(
            500, 
            HEIGHT - settings.shape_height,
            settings.shape_width,
            settings.shape_height
        )
        
        self.old_shapes_list = []
        self.last_spawn_time = time.time()
        self.rotation_angle = 0
        
        # Shape skipping state
        self.skip_current = False
        self.space_pressed = False
        
        # End game buttons
        button_width = 200
        button_height = 50
        center_x = WIDTH // 2
        self.end_buttons = [
            Button(center_x - button_width - 20, HEIGHT - 100, 
                  button_width, button_height, "Play Again"),
            Button(center_x + 20, HEIGHT - 100, 
                  button_width, button_height, "Main Menu")
        ]
        
        # Initialize fonts
        try:
            self.font = pygame.font.SysFont('Times New Roman', 20)
            self.title_font = pygame.font.SysFont('Times New Roman', 36)
        except:
            self.font = pygame.font.Font(None, 20)
            self.title_font = pygame.font.Font(None, 36)

    def draw(self):
        """Draw all shapes on the screen"""
        self.screen.fill((255, 255, 255))
        
        # Draw old shapes
        for shape, position, angle in self.old_shapes_list:
            temp_surface = pygame.Surface((self.settings.shape_width, 
                                        self.settings.shape_height), 
                                        pygame.SRCALPHA)
            temp_rect = pygame.Rect(0, 0, self.settings.shape_width, 
                                  self.settings.shape_height)
            self.shapes.shape_switchboard(shape, temp_surface, temp_rect)
            rotated_surface = pygame.transform.rotate(temp_surface, angle)
            rotated_rect = rotated_surface.get_rect(center=position.center)
            self.screen.blit(rotated_surface, rotated_rect.topleft)

        # Draw current shape if game not over
        if self.running and not self.game_over:
            temp_surface = pygame.Surface((self.settings.shape_width, 
                                        self.settings.shape_height), 
                                        pygame.SRCALPHA)
            temp_rect = pygame.Rect(0, 0, self.settings.shape_width, 
                                  self.settings.shape_height)
            self.shapes.shape_switchboard(self.current_shape, temp_surface, temp_rect)
            rotated_surface = pygame.transform.rotate(temp_surface, self.rotation_angle)
            rotated_rect = rotated_surface.get_rect(center=self.shape_rect.center)
            self.screen.blit(rotated_surface, rotated_rect.topleft)

    def draw_texts(self, time_left: int, shapes_left: int):
        """Draw the UI text elements"""
        # Draw quit instruction in top right
        quit_text = self.font.render("Press Q to quit", True, (0, 0, 0))
        quit_rect = quit_text.get_rect()
        quit_rect.topright = (self.width - 20, 20)
        self.screen.blit(quit_text, quit_rect)
        
        if self.running and not self.game_over:
            # Game info elements
            timer_surface = self.font.render(f"Time left for this shape: {time_left}", True, (0, 0, 0))
            shapes_left_surface = self.font.render(f"Shapes left: {shapes_left}", True, (0, 0, 0))
            spacebar_text = self.font.render("Press SPACEBAR to place shape", True, (0, 0, 0))
            
            self.screen.blit(timer_surface, (10, 20))
            self.screen.blit(shapes_left_surface, (10, 45))
            self.screen.blit(spacebar_text, (10, 70))
        elif self.game_over:
            # Draw end game text and buttons
            title_text = self.title_font.render("Your Masterpiece is Complete!", True, (0, 0, 0))
            title_rect = title_text.get_rect(center=(WIDTH//2, 60))
            self.screen.blit(title_text, title_rect)
            
            # Draw end game buttons
            for button in self.end_buttons:
                button.draw(self.screen)

    def handle_movement(self):
        """Handle keyboard input for shape movement"""
        keys = pygame.key.get_pressed()
        
        if keys[CONTROLS["move_left"]] and self.shape_rect.x - self.settings.shape_velocity >= 0:
            self.shape_rect.x -= self.settings.shape_velocity
        if keys[CONTROLS["move_right"]] and self.shape_rect.x + self.settings.shape_velocity + self.settings.shape_width <= WIDTH:
            self.shape_rect.x += self.settings.shape_velocity
        if keys[CONTROLS["move_up"]] and self.shape_rect.y - self.settings.shape_velocity >= 0:
            self.shape_rect.y -= self.settings.shape_velocity
        if keys[CONTROLS["move_down"]] and self.shape_rect.y + self.settings.shape_velocity + self.settings.shape_height <= HEIGHT:
            self.shape_rect.y += self.settings.shape_velocity
            
        if keys[CONTROLS["rotate_left"]]:
            self.rotation_angle += self.settings.rotation_speed
        if keys[CONTROLS["rotate_right"]]:
            self.rotation_angle -= self.settings.rotation_speed

    def handle_shape_skip(self):
        """Handle space bar press for shape skipping"""
        keys = pygame.key.get_pressed()
        if keys[CONTROLS["skip_shape"]]:
            if not self.space_pressed:
                self.skip_current = True
                self.space_pressed = True
        else:
            self.space_pressed = False
        return self.skip_current

    def reset_game(self):
        """Reset the game to start a new round"""
        # Generate new shapes
        self.shapes_list = self.shapes.shape_sequence(length=self.settings.num_shapes)
        self.shape_idx = 0
        self.current_shape = self.shapes_list[self.shape_idx]
        
        # Reset position and state
        self.shape_rect = pygame.Rect(
            500, 
            HEIGHT - self.settings.shape_height,
            self.settings.shape_width,
            self.settings.shape_height
        )
        self.old_shapes_list = []
        self.last_spawn_time = time.time()
        self.rotation_angle = 0
        
        # Reset game state
        self.game_over = False
        self.running = True
        
    async def run(self):
        """Main game loop"""
        while self.running:
            current_time = time.time()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Q key to quit
                        self.running = False
                        return "menu"
                
                # Handle end game buttons if game is over
                if self.game_over:
                    for i, button in enumerate(self.end_buttons):
                        if button.handle_event(event):
                            if i == 0:  # Play Again
                                self.reset_game()
                            else:  # Main Menu
                                self.running = False
                                return "menu"

            # Active gameplay
            if not self.game_over:
                # Game logic
                self.skip_current = self.handle_shape_skip()
                self.handle_movement()
                
                time_left = int(self.settings.spawn_delay - 
                              (current_time - self.last_spawn_time) + 1)
                
                # Shape transition logic
                if current_time - self.last_spawn_time > self.settings.spawn_delay or self.skip_current:
                    # Store current shape in old shapes list
                    self.old_shapes_list.append((
                        self.current_shape,
                        self.shape_rect.copy(),
                        self.rotation_angle
                    ))
                    
                    # Move to next shape
                    self.shape_idx += 1
                    if self.shape_idx >= len(self.shapes_list):
                        # Game is over, show end screen
                        self.game_over = True
                    else:
                        # Reset position and rotation for new shape
                        self.current_shape = self.shapes_list[self.shape_idx]
                        self.shape_rect.x = 500
                        self.shape_rect.y = HEIGHT - self.settings.shape_height
                        self.rotation_angle = 0
                        self.last_spawn_time = current_time
                        self.skip_current = False

            # Drawing
            shapes_left = self.settings.num_shapes - self.shape_idx
            self.draw()
            self.draw_texts(time_left, shapes_left)
            
            # Web-specific: update display and give control back to browser
            pygame.display.flip()
            await asyncio.sleep(0)
            
            self.clock.tick(FPS)

        return "menu"  # Return to menu when game ends